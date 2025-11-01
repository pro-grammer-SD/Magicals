import streamlit as st
from utils.supabase_client import supabase
import pandas as pd

st.title("📊 Analytics")

user = st.session_state.get("user")
if not user:
    st.warning("Please log in first!")
    st.stop()

res = supabase.table("magicals").select("title, views, likes_count, comments_count").eq("owner_id", user["id"]).execute()
data = res.data or []

if not data:
    st.info("No magicals uploaded yet.")
else:
    df = pd.DataFrame(data)
    st.dataframe(df)
