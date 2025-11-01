import streamlit as st
from utils.supabase_client import supabase

st.set_page_config(page_title="🔐 Auth", page_icon="🔑")
st.title("🔐 Login / Sign Up")

if "user" not in st.session_state:
    st.session_state.user = None

action = st.radio("Choose Action", ["Login", "Sign Up"], horizontal=True)
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button(action):
    if not email or not password:
        st.error("Please fill in both email and password.")
    else:
        try:
            if action == "Sign Up":
                res = supabase.auth.sign_up({"email": email, "password": password})
                if res.user:
                    st.success("✅ Account created! Check your email to verify before logging in.")
                else:
                    st.warning("⚠️ Check your inbox for the verification email before signing in.")

            else:  # Login
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                if res.user:
                    st.session_state.user = {"id": res.user.id, "email": res.user.email}
                    st.success(f"Welcome back, {res.user.email}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials or unverified email.")

        except Exception as e:
            st.error(f"Error: {str(e)}")

if st.session_state.user:
    st.markdown(f"✅ Logged in as **{st.session_state.user['email']}**")
    if st.button("Logout"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
        