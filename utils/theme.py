import streamlit as st

def theme_toggle():
    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "light"

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        toggle = st.toggle("🌗 Dark Mode", value=(st.session_state["theme_mode"] == "dark"))

    if toggle:
        st.session_state["theme_mode"] = "dark"
        st.markdown(
            """
            <style>
            body { background-color: #0E1117; color: white; }
            .stButton>button { background-color: #262730; color: white; }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.session_state["theme_mode"] = "light"
        st.markdown(
            """
            <style>
            body { background-color: white; color: black; }
            .stButton>button { background-color: #f0f2f6; color: black; }
            </style>
            """,
            unsafe_allow_html=True,
        )
        