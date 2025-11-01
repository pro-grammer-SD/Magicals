import streamlit as st
from utils.supabase_client import supabase
from utils.theme import theme_toggle
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Analytics", layout="wide")
theme_toggle()
st.title("📈 Analytics")

videos = supabase.table("videos").select("likes, views, comments").execute().data or []
if not videos:
    st.info("No videos yet.")
else:
    df = pd.DataFrame(videos)
    fig = px.bar(df, y="likes", title="Likes per Magical")
    st.plotly_chart(fig)
    