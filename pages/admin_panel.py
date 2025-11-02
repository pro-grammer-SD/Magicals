import os
import streamlit as st
from utils.supabase_client import supabase
from utils.user_utils import ADMINS
st.set_page_config(page_title="admin")
user = st.session_state.get("user")
if not user or user.get("email") not in ADMINS:
    st.error("admin only")
    st.stop()
st.title("moderation")
reports = supabase.table("reports").select("*").order("timestamp", desc=True).execute().data or []
for r in reports:
    with st.expander(r.get("path","")):
        st.markdown(f"reported by: {r.get('reported_by')}")
        st.markdown(f"ts: {r.get('timestamp')}")
        if st.button("ban user", key=r.get("id","ban")):
            try:
                path = r.get("path")
                meta_path = path.replace(".mp4",".json")
                if os.path.exists(meta_path):
                    import json
                    with open(meta_path) as f:
                        meta = json.load(f)
                    supabase.table("users").update({"banned": True}).eq("id", meta.get("user_id")).execute()
                    st.success("banned")
            except Exception as e:
                st.error(str(e))
        if st.button("unban user", key=r.get("id","unban")):
            try:
                path = r.get("path")
                meta_path = path.replace(".mp4",".json")
                if os.path.exists(meta_path):
                    import json
                    with open(meta_path) as f:
                        meta = json.load(f)
                    supabase.table("users").update({"banned": False}).eq("id", meta.get("user_id")).execute()
                    st.success("unbanned")
            except Exception as e:
                st.error(str(e))
