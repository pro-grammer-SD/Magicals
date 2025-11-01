import streamlit as st
from utils.render_manim import render_manim_code
from utils.supabase_client import supabase
from utils.theme import theme_toggle

st.set_page_config(page_title="Create Magical", layout="wide")
theme_toggle()
st.title("🎨 Create a Magical")

username = st.text_input("Username")
code = st.text_area("Enter Manim code here (include Scene class)")
if st.button("Render Magical"):
    path = render_manim_code(code)
    if path and path.endswith(".mp4"):
        st.video(path)
        if st.button("Upload to Magicals"):
            supabase.storage.from_("videos").upload(f"{username}/{path.split('/')[-1]}", open(path, "rb"))
            supabase.table("videos").insert({
                "username": username,
                "video_url": path,
                "likes": 0,
                "comments": []
            }).execute()
            st.success("Uploaded successfully!")
    else:
        st.error(path)
        