import os
import toml
import streamlit as st
from supabase import create_client

def get_client():
    if "supabase" in st.secrets:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
    else:
        path = os.path.join(os.getcwd(), "secrets.toml")
        data = toml.load(path)
        url = data["supabase"]["url"]
        key = data["supabase"]["key"]
    return create_client(url, key)

supabase = get_client()

def current_user():
    u = st.session_state.get("user")
    if not u:
        return None
    try:
        r = supabase.table("profiles").select("*").eq("id", u["id"]).limit(1).execute()
        return r.data[0] if r.data else None
    except:
        return None
