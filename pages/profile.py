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

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💾 Save Changes"):
        supabase.table("profiles").upsert({
            "id": user["id"],
            "username": username,
            "bio": bio
        }).execute()
        st.success("Profile updated!")

with col2:
    if st.button("🚪 Log Out"):
        st.session_state.pop("user", None)
        st.success("You’ve been logged out.")
        st.rerun()

with col3:
    if st.button("🗑️ Delete Profile", type="primary"):
        confirm = st.checkbox("Confirm delete")
        if confirm:
            supabase.table("profiles").delete().eq("id", user["id"]).execute()
            st.session_state.pop("user", None)
            st.warning("Profile deleted permanently.")
            st.rerun()
            