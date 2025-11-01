import streamlit as st
from utils.supabase_client import supabase
from utils.theme import theme_toggle

st.set_page_config(page_title="Upload", layout="wide")
theme_toggle()
st.title("📤 Upload Magical")

username = st.text_input("Username")
video = st.file_uploader("Select MP4", type=["mp4"])
if video and st.button("Upload"):
    path = f"{username}/{video.name}"
    supabase.storage.from_("videos").upload(path, video)
    supabase.table("videos").insert({"username": username, "video_url": path, "likes": 0, "comments": []}).execute()
    st.success("Uploaded successfully!")
    