import streamlit as st
from utils.supabase_client import supabase

st.set_page_config(page_title="Magicals", page_icon="✨", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

st.title("✨ Magicals Portal")

if st.session_state.user:
    st.sidebar.success(f"Logged in as {st.session_state.user['email']}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
    st.sidebar.page_link("pages/discover.py", label="Discover 🪄")
    st.sidebar.page_link("pages/upload.py", label="Upload ⬆️")
    st.sidebar.page_link("pages/analytics.py", label="Analytics 📊")
    st.sidebar.page_link("pages/profile.py", label="Profile 👤")
else:
    st.sidebar.warning("Please log in to access pages")
    st.switch_page("pages/auth.py")
