import streamlit as st
from utils.supabase_client import supabase

st.set_page_config(page_title="Login / Signup", layout="centered")
st.title("🔐 Login / Sign Up")

mode = st.radio("", ["Login", "Sign Up"], horizontal=True)
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button(mode):
    if not email or not password:
        st.error("Please fill all fields.")
    else:
        try:
            if mode == "Sign Up":
                res = supabase.auth.sign_up({"email": email, "password": password})
                if res and res.user:
                    st.success("✅ Account created. Please verify your email before logging in.")
                else:
                    st.warning("Check your inbox for verification link.")
            else:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                if res and res.user:
                    st.session_state.user = {"id": res.user.id, "email": res.user.email}
                    st.success(f"Welcome {res.user.email}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        except Exception as e:
            st.error(str(e))
            