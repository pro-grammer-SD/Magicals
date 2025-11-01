import streamlit as st

def navbar():
    st.sidebar.title("✨ Magicals")
    st.sidebar.page_link("pages/discover.py", label="Discover")
    st.sidebar.page_link("pages/upload.py", label="Upload")
    st.sidebar.page_link("pages/editor.py", label="Create Magical")
    st.sidebar.page_link("pages/analytics.py", label="Analytics")
    st.sidebar.page_link("pages/profile.py", label="Profile")
    