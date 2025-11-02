import streamlit as st
st.set_page_config(page_title="magicals", layout="wide")
st.title("magicals")
st.write("use the sidebar to navigate")
with st.sidebar:
    st.button("discover")
