import streamlit as st
from utils.supabase_client import supabase

st.title("🔐 Login / Sign Up")

action = st.radio("Choose Action", ["Login", "Sign Up"], horizontal=True)
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button(action):
    try:
        if action == "Sign Up":
            supabase.auth.sign_up({"email": email, "password": password})
            st.success("✅ Account created! Verify your email before login.")
        else:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state.user = {"id": user.user.id, "email": user.user.email}
            st.experimental_rerun()
    except Exception as e:
        st.error(str(e))
