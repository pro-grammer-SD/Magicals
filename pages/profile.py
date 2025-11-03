import streamlit as st
from pathlib import Path
from datetime import datetime
from utils.supabase_client import supabase

PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_AVATAR = PROJECT_ROOT / "assets" / "def_pfp.png"

st.set_page_config(page_title="Profile")
params = st.query_params
username = params.get("username", [None])[0] if isinstance(params.get("username"), list) else params.get("username")

if not username and st.session_state.get("user"):
    p = supabase.table("profiles").select("username").eq("id", st.session_state["user"]["id"]).execute()
    username = p.data[0]["username"] if p.data else None

if not username:
    st.error("No username provided.")
    st.stop()

res = supabase.table("profiles").select("*").eq("username", username).execute()
if not res.data:
    st.error("User not found.")
    st.stop()

profile = res.data[0]
avatar_url = profile.get("avatar_url") or str(DEFAULT_AVATAR)
if avatar_url.startswith("http"):
    avatar_url += f"?v={int(datetime.utcnow().timestamp())}"

st.image(avatar_url, width=128)
st.markdown(f"# @{profile.get('username')}")
st.markdown(profile.get("bio", ""))

user = st.session_state.get("user")
if user and user.get("id") == profile.get("id"):
    uploaded = st.file_uploader("Change Profile Picture", type=["jpg", "jpeg", "png"])
    if uploaded and st.button("Upload New Avatar"):
        bucket = "profile_pics"
        ext = uploaded.name.split(".")[-1].lower()
        file_name = f"{username}_{int(datetime.utcnow().timestamp())}.{ext}"
        data = uploaded.read()

        supabase.storage.from_(bucket).upload(
            file_name,
            data,
            {"upsert": "true", "content-type": f"image/{ext}"}
        )

        public_url = supabase.storage.from_(bucket).get_public_url(file_name)
        supabase.table("profiles").update({"avatar_url": public_url}).eq("id", profile["id"]).execute()

        st.session_state["force_refresh"] = datetime.utcnow().timestamp()
        st.success("Profile picture updated successfully and is public.")
        st.rerun()

if "force_refresh" in st.session_state:
    res = supabase.table("profiles").select("*").eq("username", username).execute()
    if res.data:
        profile = res.data[0]

mag = supabase.table("magicals").select("*").eq("owner_id", profile["id"]).order("timestamp", desc=True).execute()
videos = mag.data if mag.data else []
total_likes = sum(v.get("likes", 0) for v in videos)
st.markdown(f"**Total likes:** {total_likes}")

for v in videos:
    st.markdown(f"### {v.get('title')}")
    st.video(v.get("url"))
    st.markdown(f"❤️ {v.get('likes', 0)}")
    