import os
import tempfile
import subprocess
import uuid

def render_manim_code(code: str):
    tempdir = tempfile.mkdtemp()
    script_path = os.path.join(tempdir, f"scene_{uuid.uuid4().hex}.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)
    try:
        subprocess.run(["manim", "-pql", script_path, "Scene"], check=True)
        video_dir = os.path.join(tempdir, "media", "videos", "scene", "480p15")
        for file in os.listdir(video_dir):
            if file.endswith(".mp4"):
                return os.path.join(video_dir, file)
    except subprocess.CalledProcessError as e:
        return f"Render failed: {e}"
    