import streamlit as st
from streamlit_shadcn_ui import tabs, card, button, alert
from utils.supabase_client import supabase
from streamlit_cookies_manager import EncryptedCookieManager

# Initialize cookies
cookies = EncryptedCookieManager(prefix="magicals_", password="secret-key-auth")
if not cookies.ready():
    st.stop()

# Page config
st.set_page_config(
    page_title="Login / Signup",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stApp {
        background: transparent;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 500px;
    }
</style>
""", unsafe_allow_html=True)

# Check for existing session
if "user" not in st.session_state and cookies.get("access_token"):
    try:
        session = supabase.auth.get_user(cookies.get("access_token"))
        if session and session.user:
            st.session_state.user = {"id": session.user.id, "email": session.user.email}
    except Exception:
        cookies["access_token"] = ""
        cookies.save()

# Logged in view
if "user" in st.session_state:
    with card(key="logged_in_card"):
        st.markdown("### 🎉 Welcome Back!")
        st.markdown(f"**Email:** {st.session_state.user['email']}")
        st.markdown(f"**User ID:** `{st.session_state.user['id'][:8]}...`")
        
        alert(
            text=f"You're logged in as {st.session_state.user['email']}",
            variant="success",
            key="success_alert"
        )
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if button("🚪 Logout", key="logout_btn", variant="destructive"):
                cookies["access_token"] = ""
                cookies.save()
                st.session_state.clear()
                st.rerun()
    
    st.stop()

# Auth page - Everything inside a card
with card(key="auth_card"):
    # Header
    st.markdown("<h1 style='text-align: center; margin-bottom: 0.5rem;'>🔐 Welcome</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; margin-bottom: 2rem;'>Sign in to your account or create a new one</p>", unsafe_allow_html=True)
    
    # Tabs for Login/Signup
    tab = tabs(
        options=["Login", "Sign Up"],
        default_value="Login",
        key="auth_tabs"
    )
    
    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Form inputs
    st.markdown("#### Email Address")
    email = st.text_input(
        "Email",
        placeholder="Enter your email",
        key="email_field",
        label_visibility="collapsed"
    )
    
    st.markdown("#### Password")
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        key="password_field",
        label_visibility="collapsed"
    )
    
    # Add spacing
    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if tab == "Login":
            submit = button("🔓 Sign In", key="login_btn", variant="default")
        else:
            submit = button("✨ Create Account", key="signup_btn", variant="default")
    
    # Handle form submission
    if submit:
        if not email or not password:
            alert(
                text="⚠️ Please fill in all fields",
                variant="destructive",
                key="error_alert"
            )
        else:
            try:
                if tab == "Sign Up":
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    if res.user:
                        alert(
                            text="✅ Account created! Please check your email to verify your account.",
                            variant="success",
                            key="signup_success"
                        )
                        st.balloons()
                else:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    if res.user:
                        cookies["access_token"] = res.session.access_token
                        cookies.save()
                        st.session_state.user = {"id": res.user.id, "email": res.user.email}
                        alert(
                            text=f"🎉 Welcome back, {res.user.email}!",
                            variant="success",
                            key="login_success"
                        )
                        st.balloons()
                        st.rerun()
                    else:
                        alert(
                            text="❌ Invalid credentials. Please try again.",
                            variant="destructive",
                            key="invalid_creds"
                        )
            except Exception as e:
                error_msg = str(e)
                # Make error messages more user-friendly
                if "Email not confirmed" in error_msg:
                    error_msg = "Please verify your email before logging in. Check your inbox for the verification link."
                elif "Invalid login credentials" in error_msg:
                    error_msg = "Invalid email or password. Please try again."
                elif "User already registered" in error_msg:
                    error_msg = "This email is already registered. Please login instead."
                
                alert(
                    text=f"⚠️ {error_msg}",
                    variant="destructive",
                    key="auth_error"
                )
    
    # Footer
    st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #eee;'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #999; font-size: 0.85rem;'>Protected by magic 🪄</p>", unsafe_allow_html=True)
    