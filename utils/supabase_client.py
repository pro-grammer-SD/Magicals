import os
import toml
import streamlit as st
from supabase import create_client

def get_client():
    if "supabase" in st.secrets:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
    else:
        secrets = toml.load("../streamlit/secrets.toml")
        url = secrets["supabase"]["url"]
        key = secrets["supabase"]["key"]
    return create_client(url, key)

supabase = get_client()
