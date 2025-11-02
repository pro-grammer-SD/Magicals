import streamlit as st
from pathlib import Path
from utils.supabase_client import supabase

PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_AVATAR = PROJECT_ROOT / "assets" / "def_pfp.png"

st.set_page_config(page_title="Community")
st.title("Community")

res = supabase.table("profiles").select("id,username,avatar_url").execute()
users = res.data if res.data else []

cols = st.columns(4)
i = 0
for u in users:
    with cols[i % 4]:
        st.image(u.get("avatar_url") or str(DEFAULT_AVATAR), width=96)
        st.markdown(f"### [{u.get('username')}](profile?username={u.get('username')})")
    i += 1
    