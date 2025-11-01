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
                    progress_bar = st.progress(0, text="Starting render...")
                    progress_placeholder = st.empty()

                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            cmd = [
                                "manim",
                                temp_path,
                                scene_name,
                                "-qp",
                                "-o",
                                "output.mp4",
                                "--media_dir",
                                tmpdir,
                            ]

                            process = subprocess.Popen(
                                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
                            )

                            total_steps = 10
                            step = 0
                            for line in process.stdout:
                                line = line.strip()
                                if "Animation" in line or "File ready at" in line:
                                    step = min(step + 1, total_steps)
                                    progress = int((step / total_steps) * 100)
                                    progress_bar.progress(progress / 100, text=f"Rendering... {progress}%")

                                progress_placeholder.text(line)

                            process.wait()

                            if process.returncode == 0:
                                progress_bar.progress(1.0, text="✅ Render complete!")
                                progress_bar.empty()
                                progress_placeholder.empty()
                                output_path = os.path.join(tmpdir, "videos", scene_name, "1440p60", "output.mp4")
                                if os.path.exists(output_path):
                                    st.success("Render complete!")
                                    st.video(output_path)
                                else:
                                    st.error("No video found after render.")
                            else:
                                progress_bar.progress(1.0, text="❌ Render failed.")
                                st.error("Manim render failed!")

                    except Exception as e:
                        progress_bar.progress(1.0, text="❌ Error during render.")
                        st.error(f"Render error: {e}")
                        