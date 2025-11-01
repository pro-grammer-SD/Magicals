import streamlit as st
import os
import tempfile
import subprocess

st.title("🎬 Manim Renderer or Video Uploader")

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
option = st.radio("Choose mode:", ["Upload Video", "Upload .py Manim Script"])

if option == "Upload Video":
    uploaded_video = st.file_uploader("Upload MP4 (max 10 MB)", type=["mp4"])
    if uploaded_video:
        if uploaded_video.size > MAX_FILE_SIZE:
            st.error("File too large! Must be under 10 MB.")
        else:
            st.video(uploaded_video)

else:
    uploaded_script = st.file_uploader("Upload Manim .py file (max 10 MB)", type=["py"])
    if uploaded_script:
        if uploaded_script.size > MAX_FILE_SIZE:
            st.error("File too large! Must be under 10 MB.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
                temp_file.write(uploaded_script.read())
                temp_path = temp_file.name

            scene_name = st.text_input("Enter Scene Class Name (from your .py file):")

            if st.button("Render"):
                if not scene_name.strip():
                    st.error("Please enter a valid scene name.")
                else:
                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            cmd = [
                                "manim",
                                temp_path,
                                scene_name,
                                "-qm",
                                "-o",
                                "output.mp4",
                                "--media_dir",
                                tmpdir,
                            ]
                            subprocess.run(cmd, check=True)
                            output_path = os.path.join(tmpdir, "videos", scene_name, "480p15", "output.mp4")
                            if os.path.exists(output_path):
                                st.success("Render complete!")
                                st.video(output_path)
                            else:
                                st.error("No video found after render.")
                    except subprocess.CalledProcessError as e:
                        st.error(f"Render failed: {e}")
                        