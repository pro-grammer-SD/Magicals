import streamlit as st
from utils.supabase_client import supabase

st.set_page_config(page_title="Login / Signup", layout="centered")
st.title("🔐 Login / Signup")

if "user" in st.session_state:
    st.success(f"Logged in as {st.session_state.user['email']}")
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
else:
    mode = st.radio("Select mode", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button(mode):
        if not email or not password:
            st.error("Please fill all fields.")
        else:
            try:
                if mode == "Sign Up":
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    if res.user:
                        st.success("✅ Account created. Please verify your email before logging in.")
                else:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    if res.user:
                        st.session_state.user = {"id": res.user.id, "email": res.user.email}
                        st.success(f"Welcome {res.user.email}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
            except Exception as e:
                st.error(f"Auth error: {str(e)}")
                