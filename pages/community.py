import streamlit as st
from utils.supabase_client import supabase
st.set_page_config(page_title="community")
st.title("community")
res = supabase.table("profiles").select("id,username,profile_pic_url").execute()
users = res.data if res.data else []
cols = st.columns(4)
i=0
for u in users:
    with cols[i%4]:
        st.image(u.get("profile_pic_url") or "https://via.placeholder.com/96", width=96)
        st.markdown(f\"### [{u.get('username')}](profile?username={u.get('username')})\")
    i+=1
