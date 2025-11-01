import streamlit as st

def theme_toggle():
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    if st.sidebar.toggle("🌙 Dark Mode", st.session_state.dark_mode):
        st.session_state.dark_mode = True
    else:
        st.session_state.dark_mode = False
    st.markdown(
        f"<style>body{{background-color:{'#0E1117' if st.session_state.dark_mode else 'white'};color:{'white' if st.session_state.dark_mode else 'black'};}}</style>",
        unsafe_allow_html=True,
    )
    