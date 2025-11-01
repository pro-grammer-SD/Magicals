import os
import uuid
import tempfile
import subprocess
import streamlit as st
from utils.supabase_client import supabase

st.title("⬆️ Upload Magical")

user = st.session_state.get("user")
if not user:
    st.warning("Please log in first!")
    st.stop()

title = st.text_input("Title", placeholder="Enter your Magical title")
desc = st.text_area("Description", placeholder="Describe your Magical")
choice = st.radio("Select Input Type", ["🎥 Upload Video", "💻 Render Code"])

video_url = ""
code_url = ""

if choice == "🎥 Upload Video":
    uploaded_file = st.file_uploader("Upload your video", type=["mp4", "mov", "mkv"])
    if uploaded_file:
        path = f"videos/{uuid.uuid4()}.mp4"
        with st.spinner("Uploading..."):
            supabase.storage.from_("magicals").upload(path, uploaded_file)
        video_url = supabase.storage.from_("magicals").get_public_url(path)
        st.video(video_url)
        st.success("Video uploaded successfully!")

elif choice == "💻 Render Code":
    code = st.text_area("Enter your Manim code", height=300, placeholder="Write your Scene class here...")
    if st.button("Render"):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "render_scene.py")
            with open(file_path, "w") as f:
                f.write(code)
            try:
                subprocess.run(["manim", "-pql", file_path, "Scene"], check=True, cwd=tmpdir)
                video_path = os.path.join(tmpdir, "media/videos/render_scene/480p15/Scene.mp4")
                if os.path.exists(video_path):
                    path = f"videos/{uuid.uuid4()}.mp4"
                    with open(video_path, "rb") as f:
                        supabase.storage.from_("magicals").upload(path, f)
                    video_url = supabase.storage.from_("magicals").get_public_url(path)
                    st.video(video_url)
                    st.success("Rendered and uploaded successfully!")
                else:
                    st.error("Render failed — no video found.")
            except subprocess.CalledProcessError as e:
                st.error(f"Render error: {e}")

if st.button("Save Magical"):
    if not title or not video_url:
        st.error("Please fill all required fields and ensure a video is uploaded/rendered!")
    else:
        supabase.table("magicals").insert({
            "id": str(uuid.uuid4()),
            "owner_id": user["id"],
            "title": title,
            "description": desc,
            "video_url": video_url,
            "code_url": code_url
        }).execute()
        st.success("🎉 Magical saved successfully!")
        