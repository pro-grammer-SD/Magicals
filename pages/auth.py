import streamlit as st
from streamlit_shadcn_ui import card, tabs, button, alert
from utils.supabase_client import supabase
from streamlit_cookies_manager import EncryptedCookieManager

# ---------------- COOKIE SETUP ----------------
cookies = EncryptedCookieManager(prefix="magicals_", password="secret-key-auth")
if not cookies.ready():
    st.stop()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Login / Signup", layout="centered")

# ---------------- STYLING ----------------
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 2rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .block-container {
        max-width: 500px;
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION VALIDATION ----------------
if "user" not in st.session_state and cookies.get("access_token"):
    try:
        token = cookies.get("access_token")
        session = supabase.auth.get_user(token)
        if session and getattr(session, "user", None):
            st.session_state.user = {"id": session.user.id, "email": session.user.email}
            alert(title=f"🎉 Welcome back, {session.user.email}!", variant="success", key="welcome_back")
    except Exception:
        if "access_token" in cookies:
            del cookies["access_token"]
            cookies.save()

# ---------------- LOGGED-IN VIEW ----------------
if "user" in st.session_state:
    with card(key="logged_in_card"):
        st.markdown("### 🎉 You’re Logged In")
        st.markdown(f"**Email:** {st.session_state.user['email']}")
        st.markdown(f"**User ID:** `{st.session_state.user['id'][:8]}...`")

        alert(title=f"You're logged in as {st.session_state.user['email']}", variant="success", key="logged_in_alert")
        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if button("🚪 Logout", variant="destructive", key="logout_btn"):
                try:
                    supabase.auth.sign_out()
                except Exception:
                    pass
                if "access_token" in cookies:
                    del cookies["access_token"]
                cookies.save()
                st.session_state.clear()
                st.rerun()
    st.stop()

# ---------------- AUTH FORM ----------------
with card(key="auth_card"):
    st.markdown("<h2 style='text-align: center;'>🔐 Login / Sign Up</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Access your account below</p>", unsafe_allow_html=True)

    # Tabs for mode selection
    mode = tabs(options=["Login", "Sign Up"], default_value="Login", key="auth_tabs")

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="Enter your email", label_visibility="collapsed", key="email_field")
    password = st.text_input("Password", placeholder="Enter your password", type="password", label_visibility="collapsed", key="password_field")

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    # Centered button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit = button(f"{'🔓 Sign In' if mode == 'Login' else '✨ Create Account'}", key="submit_btn", variant="default")

    # Handle auth
    if submit:
        if not email or not password:
            alert(title="⚠️ Please fill all fields.", variant="destructive", key="missing_fields")
        else:
            try:
                if mode == "Sign Up":
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    if res.user:
                        alert(title="✅ Account created! Please verify your email before logging in.", variant="success", key="signup_ok")
                        st.balloons()
                else:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    if res.user and res.session:
                        cookies["access_token"] = res.session.access_token
                        cookies.save()
                        st.session_state.user = {"id": res.user.id, "email": res.user.email}
                        alert(title=f"🎉 Welcome {res.user.email}!", key="login_ok")
                        st.balloons()
                        st.rerun()
                    else:
                        alert(title="❌ Invalid credentials.", key="invalid_login")
            except Exception as e:
                msg = str(e)
                if "Email not confirmed" in msg:
                    msg = "Please verify your email before logging in."
                elif "Invalid login credentials" in msg:
                    msg = "Invalid email or password."
                elif "User already registered" in msg:
                    msg = "This email is already registered. Please login instead."
                alert(title=f"⚠️ {msg}", variant="destructive", key="auth_error")

# ---------------- FOOTER ----------------
st.markdown("<hr style='margin-top: 2rem; border: none; border-top: 1px solid #eee;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#aaa;'>Protected by magic 🪄</p>", unsafe_allow_html=True)
