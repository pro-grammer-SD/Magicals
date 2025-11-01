import streamlit as st
import os
import json
from datetime import datetime
from utils.supabase_client import supabase

st.set_page_config(page_title="🌟 Discover Magicals", page_icon="🪄")
st.header("🌟 Discover Magicals")

PUBLIC_DIR = "published_magicals"
os.makedirs(PUBLIC_DIR, exist_ok=True)

current_user = st.session_state.get("user")
user_id = current_user.get("id") if current_user else None

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
        author_id = meta.get("user_id")
        likes = meta.get("likes", 0)
        liked_by = meta.get("liked_by", [])
        timestamp = meta.get("timestamp", "")

        username = "Anonymous"
        if author_id:
            try:
                res = supabase.table("profiles").select("username").eq("id", author_id).execute()
                if res.data:
                    username = res.data[0].get("username", "Anonymous")
            except Exception:
                pass

        with st.container():
            st.markdown(f"### 🎥 {title}")
            st.markdown(f"**By:** @{username} | 🕒 {timestamp.split('T')[0] if timestamp else 'Unknown'}")
            st.video(os.path.join(PUBLIC_DIR, vid))
            if desc:
                st.markdown(f"_{desc}_")

            has_liked = user_id in liked_by if user_id else False
            like_btn_label = f"❤️ {likes} Likes" if not has_liked else f"💖 {likes} Liked"

            if st.button(like_btn_label, key=vid):
                if not user_id:
                    st.warning("You must log in to like videos.")
                elif not has_liked:
                    likes += 1
                    liked_by.append(user_id)
                    meta["likes"] = likes
                    meta["liked_by"] = liked_by
                    with open(json_path, "w") as f:
                        json.dump(meta, f, indent=4)
                    st.rerun()
                else:
                    st.info("You already liked this Magical 💫")

            st.markdown("---")
            