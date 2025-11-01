import streamlit as st
from utils.supabase_client import supabase

st.title("🪄 Discover Magicals")

res = supabase.table("magicals").select("*").order("created_at", desc=True).execute()
magicals = res.data or []

if not magicals:
    st.info("No magicals yet. Be the first to upload!")
else:
    for m in magicals:
        st.subheader(m["title"])
        st.write(m.get("description", ""))
        st.video(m.get("video_url"))
        st.markdown(f"⭐ Likes: {m.get('likes_count', 0)} | 💬 Comments: {m.get('comments_count', 0)} | 👁️ Views: {m.get('views', 0)}")
