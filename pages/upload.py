import streamlit as st
import os
import tempfile
import subprocess
import re

st.title("🎬 Manim Renderer or Video Uploader")

MAX_FILE_SIZE = 10 * 1024 * 1024
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
                    progress_bar = st.progress(0, text="Initializing render...")
                    log_box = st.empty()
                    video_path = None

                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            cmd = [
                                "manim",
                                temp_path,
                                scene_name,
                                "-ql",
                                "-o",
                                "output.mp4",
                                "--media_dir",
                                tmpdir,
                                "--progress_bar",
                                "display"
                            ]

                            process = subprocess.Popen(
                                cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True,
                                bufsize=1,
                            )

                            for line in process.stdout:
                                log_box.text(line.strip())

                                # Progress percentage live
                                percent_match = re.search(r"\[\s*(\d+)%\]", line)
                                if percent_match:
                                    percent = int(percent_match.group(1))
                                    color_text = f"Rendering... {percent}%"
                                    if percent < 100:
                                        progress_bar.progress(percent / 100, text=color_text)
                                    else:
                                        progress_bar.progress(1.0, text="✅ Render complete!")

                                # Output path live capture
                                path_match = re.search(r"File ready at\s+'([^']+)'", line)
                                if path_match:
                                    video_path = path_match.group(1).strip()

                            process.wait()

                            if process.returncode == 0 and video_path and os.path.exists(video_path):
                                progress_bar.progress(1.0, text="✅ Success!")
                                st.video(video_path)
                            elif process.returncode == 0:
                                progress_bar.progress(1.0, text="⚠️ No video found.")
                                st.error("Rendered file missing.")
                            else:
                                progress_bar.progress(1.0, text="❌ Render failed.")
                                st.error("Manim failed to render. Check your scene name/code.")

                    except Exception as e:
                        progress_bar.progress(1.0, text="❌ Error.")
                        st.error(f"Error: {e}")
                        