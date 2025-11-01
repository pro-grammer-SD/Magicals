import streamlit as st
import os
import subprocess
import re

st.title("🎬 Manim Renderer or Video Uploader")

MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024
option = st.radio("Choose mode:", ["Upload Video", "Upload .py Manim Script"])

if option == "Upload Video":
    uploaded_video = st.file_uploader("Upload MP4 (max 10 MB)", type=["mp4"])
    if uploaded_video:
        if uploaded_video.size > MAX_FILE_SIZE:
            st.error("File too large! Must be under 10 MB.")
        else:
            save_path = os.path.join(MEDIA_DIR, uploaded_video.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_video.read())
            st.success(f"✅ Uploaded successfully: {uploaded_video.name}")
            st.video(save_path)

else:
    uploaded_script = st.file_uploader("Upload Manim .py file (max 10 MB)", type=["py"])
    if uploaded_script:
        if uploaded_script.size > MAX_FILE_SIZE:
            st.error("File too large! Must be under 10 MB.")
        else:
            script_path = os.path.join(MEDIA_DIR, uploaded_script.name)
            with open(script_path, "wb") as f:
                f.write(uploaded_script.read())

            scene_name = st.text_input("Enter Scene Class Name (from your .py file):")

            if st.button("Render"):
                if not scene_name.strip():
                    st.error("Please enter a valid scene name.")
                else:
                    progress_bar = st.progress(0, text="Initializing render...")
                    log_box = st.empty()
                    video_path = None

                    try:
                        output_name = f"{os.path.splitext(uploaded_script.name)[0]}_{scene_name}.mp4"
                        output_path = os.path.join(MEDIA_DIR, output_name)

                        cmd = [
                            "manim",
                            script_path,
                            scene_name,
                            "-ql",
                            "-o",
                            output_name,
                            "--media_dir",
                            MEDIA_DIR,
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
                            line = line.strip()
                            print(line, flush=True)
                            log_box.text(line)

                            percent_match = re.search(r"\[\s*(\d+)%\]", line)
                            if percent_match:
                                percent = int(percent_match.group(1))
                                progress_bar.progress(
                                    percent / 100 if percent < 100 else 1.0,
                                    text=f"Rendering... {percent}%" if percent < 100 else "✅ Render complete!"
                                )

                            path_match = re.search(r"File ready at\s+'([^']+)'", line)
                            if path_match:
                                video_path = path_match.group(1).strip()
                                print(f"[DEBUG] Output path found: {video_path}", flush=True)

                        process.wait()

                        print(f"[DEBUG] Process return code: {process.returncode}", flush=True)
                        print(f"[DEBUG] Final video_path: {video_path}", flush=True)

                        if process.returncode == 0 and video_path and os.path.exists(video_path):
                            progress_bar.progress(1.0, text="✅ Success!")
                            st.video(video_path)
                            st.success(f"Saved at {video_path}")
                        elif os.path.exists(output_path):
                            progress_bar.progress(1.0, text="✅ Success!")
                            st.video(output_path)
                            st.success(f"Saved at {output_path}")
                        else:
                            progress_bar.progress(1.0, text="⚠️ No video found.")
                            st.error("Rendered file missing.")

                    except Exception as e:
                        progress_bar.progress(1.0, text="❌ Error.")
                        st.error(f"Error: {e}")
                        print(f"[ERROR] Exception occurred: {e}", flush=True)
                        