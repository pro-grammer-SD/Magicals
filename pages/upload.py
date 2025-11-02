import re
import streamlit as st
import os
import sys
import subprocess
import json
from datetime import datetime
from utils.supabase_client import supabase, current_user
from utils.nsfw_check import check_video_nsfw
from supabase.lib.client_options import ClientOptions

st.set_page_config(page_title="upload", layout="wide")
user = st.session_state.get("user")
if not user:
    st.warning("login first")
    st.stop()

profile = current_user()
username = profile.get("username") if profile and profile.get("username") else user["email"].split("@")[0]
bucket_name = "magical_uploads"
try:
    supabase.storage.create_bucket(bucket_name, public=True)
except Exception:
    pass

mode = st.radio("mode", ["upload video", "upload script"])

def upload_to_supabase(path, file_name):
    with open(path, "rb") as f:
        supabase.storage.from_(bucket_name).upload(file_name, f, {"upsert": True})
    return supabase.storage.from_(bucket_name).get_public_url(file_name)

media_dir = os.path.join("/home", username, "media")
os.makedirs(media_dir, exist_ok=True)

if mode == "upload video":
    uploaded = st.file_uploader("mp4", type=["mp4"])
    title = st.text_input("title")
    desc = st.text_area("description")
    if uploaded and st.button("scan & publish"):
        if uploaded.size > 50 * 1024 * 1024:
            st.error("video > 50mb")
        elif not title.strip():
            st.error("title required")
        else:
            path = os.path.join(media_dir, uploaded.name)
            with open(path, "wb") as f:
                f.write(uploaded.read())
            ok, info = check_video_nsfw(path)
            if ok:
                st.error("nsfw detected. cannot publish")
            else:
                safe_title = title.replace(" ", "_").replace("/", "_")
                cloud_path = f"{username}/{safe_title}.mp4"
                url = upload_to_supabase(path, cloud_path)
                meta = {"title": title, "description": desc, "user_id": user["id"], "username": username, "url": url, "likes": 0, "timestamp": datetime.utcnow().isoformat()}
                supabase.table("magicals").insert(meta).execute()
                st.success("published")
                st.video(url)

if mode == "upload script":
    uploaded = st.file_uploader("py", type=["py"])
    scene = st.text_input("scene class name")
    title = st.text_input("title")
    desc = st.text_area("description")
    if uploaded and st.button("render & publish"):
        if uploaded.size > 10 * 1024 * 1024:
            st.error("script > 10mb")
        elif not title.strip() or not scene.strip():
            st.error("title and scene required")
        else:
            script_path = os.path.join(media_dir, uploaded.name)
            with open(script_path, "wb") as f:
                f.write(uploaded.read())
            cmd = [sys.executable, "-m", "manim", script_path, scene, "-qp", "--media_dir", media_dir, "--progress_bar", "display"]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            logs = st.empty()
            output_path = None
            for ln in proc.stdout:
                logs.text(ln)
                match = re.search(r"(?P<path>\/[^\s]*1440p60[^\s]*\.mp4)", ln)
                if match:
                    output_path = match.group("path")
            proc.wait()
            if proc.returncode == 0 and output_path and os.path.exists(output_path):
                ok, info = check_video_nsfw(output_path)
                if ok:
                    os.remove(output_path)
                    st.error("nsfw detected in render")
                else:
                    safe_title = title.replace(" ", "_").replace("/", "_")
                    cloud_path = f"{username}/{safe_title}_{scene}.mp4"
                    url = upload_to_supabase(output_path, cloud_path)
                    meta = {"title": title, "description": desc, "user_id": user["id"], "username": username, "url": url, "likes": 0, "timestamp": datetime.utcnow().isoformat()}
                    supabase.table("magicals").insert(meta).execute()
                    st.success("rendered and published")
                    st.video(url)
            else:
                st.error("render failed or output not found")
                