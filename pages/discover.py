import streamlit as st
from utils.supabase_client import supabase
from components.video_card import video_card
from utils.theme import theme_toggle

st.set_page_config(page_title="Discover", layout="wide")
theme_toggle()
st.title("🔥 Trending Magicals")

videos = supabase.table("videos").select("*").order("created_at", desc=True).execute().data or []
for v in videos:
    video_card(v["video_url"], v["username"], v["likes"], v["comments"])
    