import streamlit as st
from utils.supabase_client import supabase

st.title("👤 Profile")

user = st.session_state.get("user")
if not user:
    st.warning("Please log in first!")
    st.stop()

res = supabase.table("profiles").select("*").eq("id", user["id"]).execute()
data = res.data[0] if res.data else {"username": "", "bio": ""}

username = st.text_input("Username", data.get("username"))
bio = st.text_area("Bio", data.get("bio"))

if st.button("Save"):
    supabase.table("profiles").upsert({
        "id": user["id"],
        "username": username,
        "bio": bio
    }).execute()
    st.success("Profile updated!")
