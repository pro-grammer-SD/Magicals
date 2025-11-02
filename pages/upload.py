import streamlit as st
import os
import sys
import subprocess
import json
import tempfile
from datetime import datetime
from utils.supabase_client import supabase, current_user
from utils.nsfw_check import check_video_nsfw
st.set_page_config(page_title="upload", layout="wide")
user = st.session_state.get("user")
if not user:
    st.warning("login first")
    st.stop()
profile = current_user()
username = profile.get("username") if profile and profile.get("username") else user["email"].split("@")[0]
base = os.path.join("/home", username, "media", "1440p60")
os.makedirs(base, exist_ok=True)
mode = st.radio("mode", ["upload video","upload script"])
if mode == "upload video":
    uploaded = st.file_uploader("mp4", type=["mp4"])
    title = st.text_input("title")
    desc = st.text_area("description")
    if uploaded and st.button("scan & publish"):
        if uploaded.size > 50*1024*1024:
            st.error("video > 50mb")
        elif not title.strip():
            st.error("title required")
        else:
            safe_title = title.replace(\" \", \"_\").replace(\"/\",\"_\")
            final = os.path.join(base, f\"{safe_title}.mp4\")
            if os.path.exists(final):
                st.error("title exists")
            else:
                tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
                tmp.write(uploaded.read())
                tmp.flush()
                ok, info = check_video_nsfw(tmp.name)
                if ok:
                    st.error("nsfw detected. cannot publish")
                else:
                    os.rename(tmp.name, final)
                    meta = {"title": title, "description": desc, "user_id": user["id"], "username": username, "path": final, "likes": 0, "timestamp": datetime.utcnow().isoformat()}
                    with open(final.replace(".mp4",".json"), "w") as f:
                        json.dump(meta, f)
                    try:
                        supabase.table("magicals").insert(meta).execute()
                    except:
                        pass
                    st.success("published")
                    st.video(final)
if mode == "upload script":
    uploaded = st.file_uploader("py", type=["py"])
    scene = st.text_input("scene class name")
    title = st.text_input("title")
    desc = st.text_area("description")
    if uploaded and st.button("render & publish"):
        if uploaded.size > 10*1024*1024:
            st.error("script > 10mb")
        elif not title.strip() or not scene.strip():
            st.error("title and scene required")
        else:
            safe_title = title.replace(\" \",\"_\").replace(\"/\",\"_\")
            tmpdir = os.path.join("/home", username, "media")
            os.makedirs(tmpdir, exist_ok=True)
            script_path = os.path.join(tmpdir, uploaded.name)
            with open(script_path, "wb") as f:
                f.write(uploaded.read())
            output_name = f\"{safe_title}_{scene}.mp4\"
            output_path = os.path.join(os.path.dirname(tmpdir), "1440p60", output_name)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cmd = [sys.executable, "-m", "manim", script_path, scene, "-qp", "-o", output_name, "--media_dir", os.path.join("/home", username, "media"), "--progress_bar", "display"]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            logs = st.empty()
            for ln in proc.stdout:
                logs.text(ln)
            proc.wait()
            if proc.returncode == 0 and os.path.exists(output_path):
                ok, info = check_video_nsfw(output_path)
                if ok:
                    os.remove(output_path)
                    st.error("nsfw detected in render")
                else:
                    meta = {"title": title, "description": desc, "user_id": user["id"], "username": username, "path": output_path, "likes": 0, "timestamp": datetime.utcnow().isoformat()}
                    with open(output_path.replace(".mp4",".json"), "w") as f:
                        json.dump(meta, f)
                    try:
                        supabase.table("magicals").insert(meta).execute()
                    except:
                        pass
                    st.success("rendered and published")
                    st.video(output_path)
            else:
                st.error("render failed")
