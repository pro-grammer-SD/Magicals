import streamlit as st
import os
import subprocess
import sys
import re
import shutil

st.set_page_config(page_title="🎬 Upload & Render", page_icon="🎥")
st.header("🎬 Upload or Render Your Magical")

MEDIA_DIR = "media"
PUBLIC_DIR = "published_magicals"
os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(PUBLIC_DIR, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024

mode = st.radio("Choose mode:", ["Upload Video", "Upload .py Manim Script"])

if mode == "Upload Video":
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

            if st.button("✨ Publish this Magical"):
                public_path = os.path.join(PUBLIC_DIR, uploaded_video.name)
                shutil.copy(save_path, public_path)
                st.success("🌟 Published! It will appear in Discover.")

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
                    progress = st.progress(0, text="Starting render…")
                    log_box = st.empty()

                    base_name = os.path.splitext(uploaded_script.name)[0]
                    output_name = f"{base_name}_{scene_name}.mp4"
                    final_path = f"media/videos/script/1440p60/{output_name}"
                    os.makedirs(os.path.dirname(final_path), exist_ok=True)

                    cmd = [
                        sys.executable, "-m", "manim",
                        script_path,
                        scene_name,
                        "-qp",
                        "-o", output_name,
                        "--media_dir", "media",
                        "--progress_bar", "display"
                    ]

                    try:
                        process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            bufsize=1,
                            env={**os.environ, "STREAMLIT_RUNTIME_DISABLED": "1"},
                        )

                        logs = []
                        progress_pattern = re.compile(r"\[\s*(\d{1,3})%\]")

                        for line in process.stdout:
                            line = line.strip()
                            logs.append(line)
                            log_box.text("\n".join(logs[-20:]))

                            match = progress_pattern.search(line)
                            if match:
                                percent = int(match.group(1))
                                progress.progress(min(percent, 100) / 100)

                        process.wait()
                        progress.progress(1.0)

                        if process.returncode == 0 and os.path.exists(final_path):
                            st.success("✅ Render complete!")
                            st.video(final_path)
                            st.info(f"Saved at {final_path}")

                            if st.button("✨ Publish this Magical"):
                                public_path = os.path.join(PUBLIC_DIR, os.path.basename(final_path))
                                shutil.copy(final_path, public_path)
                                st.success("🌟 Published! It will appear in Discover.")
                        else:
                            st.error("⚠️ Render failed or file missing. Check your Scene name or script.")

                    except Exception as e:
                        progress.progress(1.0)
                        st.error(f"Error: {e}")
                        