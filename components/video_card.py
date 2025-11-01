import streamlit as st

def video_card(video_url, username, likes=0, comments=[]):
    st.video(video_url)
    st.caption(f"@{username}")
    cols = st.columns(3)
    cols[0].button(f"❤️ {likes}")
    cols[1].button(f"💬 {len(comments)}")
    