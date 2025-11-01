import streamlit as st
import os
import subprocess

st.set_page_config(page_title="🎬 Upload & Render", page_icon="🎥")
st.header("🎬 Manim Renderer or Video Uploader")

MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

mode = st.radio("Choose mode:", ["Upload Video", "Upload .py Manim Script"])

if mode == "Upload Video":
    uploaded_video = st.file_uploader("Upload MP4 (max 10 MB)", type=["mp4"])
    if uploaded_video:
        if uploaded_video.size > MAX_FILE_SIZE:
            st.error("File too large! Must be under 10 MB.")
        else:
            path = os.path.join(MEDIA_DIR, uploaded_video.name)
            with open(path, "wb") as f:
                f.write(uploaded_video.read())
            st.success(f"✅ Uploaded successfully: {uploaded_video.name}")
            st.video(path)

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
                        "display",
                    ]

                    try:
                        process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            bufsize=1,
                        )

                        logs = []
                        for line in process.stdout:
                            line = line.rstrip()
                            logs.append(line)
                            log_box.text("\n".join(logs[-20:]))

                            digits = "".join([c for c in line if c.isdigit()])
                            if digits.isdigit():
                                percent = int(digits)
                                progress.progress(min(percent, 100) / 100)

                        process.wait()

                        if process.returncode == 0 and os.path.exists(output_path):
                            progress.progress(1.0, text="✅ Done!")
                            st.video(output_path)
                            st.success(f"Saved at {output_path}")
                        else:
                            progress.progress(1.0, text="⚠️ Render failed.")
                            st.error("Render failed or file missing. Check your Scene name.")

                    except Exception as e:
                        progress.progress(1.0, text="❌ Error.")
                        st.error(f"Error: {e}")
                        