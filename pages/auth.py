import streamlit as st
from utils.supabase_client import supabase
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(prefix="magicals_")

if not cookies.ready():
    st.stop()

st.set_page_config(page_title="Login / Signup", layout="centered")
st.title("🔐 Login / Signup")

# Try auto-login from cookie
if "user" not in st.session_state and cookies.get("access_token"):
    try:
        session = supabase.auth.get_user(cookies.get("access_token"))
        if session and session.user:
            st.session_state.user = {"id": session.user.id, "email": session.user.email}
            st.success(f"Welcome back, {session.user.email}!")
    except Exception:
        cookies.delete("access_token")
        cookies.save()

if "user" in st.session_state:
    st.success(f"Logged in as {st.session_state.user['email']}")
    if st.button("Logout"):
        cookies.delete("access_token")
        cookies.save()
        st.session_state.clear()
        st.rerun()
    st.stop()

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
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                user = res.user
                if user:
                    cookies["access_token"] = res.session.access_token
                    cookies.save()
                    st.session_state.user = {"id": user.id, "email": user.email}
                    st.success(f"Welcome {user.email}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        except Exception as e:
            st.error(f"Auth error: {str(e)}")
            