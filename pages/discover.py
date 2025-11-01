import streamlit as st
import os

st.set_page_config(page_title="🌟 Discover Magicals", page_icon="🪄")
st.header("🌟 Community Magicals")

PUBLIC_DIR = "published_magicals"
os.makedirs(PUBLIC_DIR, exist_ok=True)

videos = [v for v in os.listdir(PUBLIC_DIR) if v.endswith(".mp4")]

if videos:
    for v in videos:
        st.subheader(v)
        st.video(os.path.join(PUBLIC_DIR, v))
else:
    st.info("No Magicals yet. Go publish one from the Upload page!")
    