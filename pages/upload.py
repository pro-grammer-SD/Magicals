import streamlit as st
from utils.supabase_client import supabase
import uuid

st.title("⬆️ Upload Magical")

user = st.session_state.get("user")
if not user:
    st.warning("Please log in first!")
    st.stop()

title = st.text_input("Title")
desc = st.text_area("Description")
video_url = st.text_input("Video URL (YouTube/direct link)")
code_url = st.text_input("Code URL (optional)")

if st.button("Upload"):
    if not title or not video_url:
        st.error("Title and Video URL are required!")
    else:
        supabase.table("magicals").insert({
            "id": str(uuid.uuid4()),
            "owner_id": user["id"],
            "title": title,
            "description": desc,
            "video_url": video_url,
            "code_url": code_url
        }).execute()
        st.success("🎉 Magical uploaded successfully!")
