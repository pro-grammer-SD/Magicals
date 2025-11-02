import streamlit as st
import os
from utils.supabase_client import supabase
st.set_page_config(page_title="profile")
params = st.experimental_get_query_params()
username = params.get("username", [None])[0]
if not username and st.session_state.get("user"):
    p = supabase.table("profiles").select("username").eq("id", st.session_state["user"]["id"]).execute()
    username = p.data[0]["username"] if p.data else None
if not username:
    st.error("no username")
    st.stop()
res = supabase.table("profiles").select("*").eq("username", username).execute()
if not res.data:
    st.error("not found")
    st.stop()
profile = res.data[0]
st.image(profile.get("profile_pic_url") or "https://via.placeholder.com/128", width=128)
st.markdown(f"# @{profile.get('username')}")
st.markdown(profile.get("bio",""))
mag = supabase.table("magicals").select("*").eq("user_id", profile["id"]).order("timestamp", desc=True).execute()
videos = mag.data if mag.data else []
total_likes = sum(v.get("likes",0) for v in videos)
st.markdown(f"**total likes:** {total_likes}")
for v in videos:
    st.markdown(f"### {v.get('title')}")
    st.video(v.get("path"))
    st.markdown(f"❤️ {v.get('likes',0)}")
