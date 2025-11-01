import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="🌟 Discover Magicals", page_icon="🪄")
st.header("🌟 Discover Magicals")

PUBLIC_DIR = "published_magicals"
os.makedirs(PUBLIC_DIR, exist_ok=True)

videos = [v for v in os.listdir(PUBLIC_DIR) if v.endswith(".mp4")]
if not videos:
    st.info("No Magicals yet. Go publish one from the Upload page!")
else:
    for vid in sorted(videos, reverse=True):
        json_path = os.path.join(PUBLIC_DIR, vid.replace(".mp4", ".json"))
        meta = {}
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                meta = json.load(f)

        title = meta.get("title", "Untitled Magical")
        desc = meta.get("description", "")
        username = meta.get("username", "Anonymous")
        likes = meta.get("likes", 0)
        timestamp = meta.get("timestamp", "")

        with st.container():
            st.markdown(f"### 🎥 {title}")
            st.markdown(f"**By:** @{username} | 🕒 {timestamp.split('T')[0]}")
            st.video(os.path.join(PUBLIC_DIR, vid))
            if desc:
                st.markdown(f"_{desc}_")
            if st.button(f"❤️ {likes} Likes", key=vid):
                likes += 1
                meta["likes"] = likes
                with open(json_path, "w") as f:
                    json.dump(meta, f, indent=4)
                st.rerun()
            st.markdown("---")
            