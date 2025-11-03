import streamlit as st
from utils.supabase_client import supabase
from streamlit_js_eval import streamlit_js_eval
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import json

st.set_page_config(page_title="Login / Signup", layout="centered")
st.title("🔐 Login / Signup")

def encrypt_token(token, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(token.encode())
    data = {
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode(),
    }
    return base64.b64encode(json.dumps(data).encode()).decode()

def decrypt_token(enc_data, key):
    try:
        data = json.loads(base64.b64decode(enc_data).decode())
        cipher = AES.new(key, AES.MODE_GCM, nonce=base64.b64decode(data["nonce"]))
        return cipher.decrypt_and_verify(
            base64.b64decode(data["ciphertext"]),
            base64.b64decode(data["tag"])
        ).decode()
    except Exception:
        return None

if "key" not in st.session_state:
    st.session_state.key = get_random_bytes(16)

enc_token = streamlit_js_eval(js_expressions="localStorage.getItem('sb_token')", key="get_token")

if enc_token and "user" not in st.session_state:
    token = decrypt_token(enc_token, st.session_state.key)
    if token:
        try:
            res = supabase.auth.set_session(token)
            if res.user:
                st.session_state.user = {"id": res.user.id, "email": res.user.email}
                st.session_state.access_token = token
        except Exception:
            streamlit_js_eval(js_expressions="localStorage.removeItem('sb_token')", key="clear_bad_token")

if "user" in st.session_state:
    st.success(f"Logged in as {st.session_state.user['email']}")
    if st.button("Logout"):
        supabase.auth.sign_out()
        streamlit_js_eval(js_expressions="localStorage.removeItem('sb_token')", key="logout_clear")
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
                        st.session_state.access_token = res.session.access_token
                        enc_token = encrypt_token(res.session.access_token, st.session_state.key)
                        streamlit_js_eval(js_expressions=f"localStorage.setItem('sb_token', '{enc_token}')", key="save_token")
                        st.success(f"Welcome {res.user.email}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
            except Exception as e:
                st.error(f"Auth error: {str(e)}")
                