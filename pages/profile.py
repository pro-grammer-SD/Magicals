import streamlit as st
from utils.supabase_client import supabase
from utils.theme import theme_toggle

st.set_page_config(page_title="Profile", layout="wide")
theme_toggle()
st.title("👤 Profile")

username = st.text_input("Username")
bio = st.text_area("Bio")
if st.button("Save"):
    supabase.table("profiles").upsert({"username": username, "bio": bio}).execute()
    st.success("Profile updated!")
    