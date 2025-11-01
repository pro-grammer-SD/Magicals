import streamlit as st
import os
import subprocess

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
                    st.info("⚙️ Rendering in progress... Output will appear below.")
                    log_output = st.empty()

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

                        full_log = ""
                        for line in process.stdout:
                            full_log += line
                            log_output.text(full_log)
                            print(line, end="", flush=True)

                        process.wait()

                        if process.returncode == 0:
                            if os.path.exists(output_path):
                                st.success("✅ Render complete!")
                                st.video(output_path)
                            else:
                                st.warning("⚠️ Render finished but output video not found.")
                        else:
                            st.error("❌ Render failed. Check console/logs above.")

                    except Exception as e:
                        st.error(f"💥 Error: {e}")
                        print(f"[ERROR] {e}", flush=True)
                        