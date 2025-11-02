import streamlit as st
from utils.supabase_client import supabase

st.set_page_config(page_title="Login / Signup", layout="centered")
st.title("🔐 Login / Signup")

mode = st.radio(
    "Select mode",
    ["Login", "Sign Up"],
    horizontal=True,
    label_visibility="collapsed"
)

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button(mode):
    if not email or not password:
        st.error("Please fill all fields.")
    else:
        try:
            if mode == "Sign Up":
                res = supabase.auth.sign_up({"email": email, "password": password})
                user = res.user
                if user:
                    st.success("✅ Account created. Please verify your email before logging in.")
                else:
                    st.warning("Sign up may have failed. Check your inbox or try again.")
            else:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                user = res.user
                if user:
                    st.session_state.user = {"id": user.id, "email": user.email}
                    st.success(f"Welcome {user.email}!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials or no response.")
        except Exception as e:
            st.error(f"Auth error: {str(e)}")
            