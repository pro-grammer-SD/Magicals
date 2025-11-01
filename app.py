import streamlit as st
from components.navbar import navbar
from utils.theme import theme_toggle

st.set_page_config(page_title="Magicals", layout="wide")
theme_toggle()
navbar()
st.title("✨ Magicals — The AI-powered Manim Community")
st.write("Create, render, and share your mathematical animations.")
