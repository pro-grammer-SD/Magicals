import os
import toml
import streamlit as st
from supabase import create_client

def get_client():
    try:
        if "supabase" in st.secrets:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
        else:
            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            paths = [
                os.path.join(root, "secrets.toml"),
                os.path.join(root, "streamlit", "secrets.toml"),
            ]
            secrets_file = next((p for p in paths if os.path.exists(p)), None)
            if not secrets_file:
                raise FileNotFoundError("No secrets.toml found.")
            secrets = toml.load(secrets_file)
            url = secrets["supabase"]["url"]
            key = secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Supabase init failed: {e}")
        return None

supabase = get_client()

def get_current_user():
    session = st.session_state.get("session")
    if not session or "user" not in session:
        return None
    return session["user"]
