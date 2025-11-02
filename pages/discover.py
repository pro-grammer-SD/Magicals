import streamlit as st
import os
import json
from utils.supabase_client import supabase

st.set_page_config(page_title="discover", layout="wide")
st.title("discover")

base = "/home"
entries = []
for u in os.listdir(base):
    media_dir = os.path.join(base, u, "media", "1440p60")
    if not os.path.exists(media_dir):
        continue
    for f in os.listdir(media_dir):
        if f.endswith(".mp4"):
            p = os.path.join(media_dir, f)
            j = p.replace(".mp4", ".json")
            meta = {}
            if os.path.exists(j):
                try:
                    with open(j, "r") as fh:
                        meta = json.load(fh)
                except:
                    meta = {}
            entries.append({"user_folder": u, "path": p, "meta": meta})

if not entries:
    st.info("no magicals yet")
else:
    for e in sorted(entries, key=lambda x: x["meta"].get("timestamp", ""), reverse=True):
        m = e["meta"]
        title = m.get("title", "untitled")
        desc = m.get("description", "")
        uname = m.get("username", e["user_folder"])
        likes = m.get("likes", 0)
        uid = m.get("user_id")

        profile = supabase.table("profiles").select("username,profile_pic_url,bio,id").eq("id", uid).execute()
        pdata = profile.data[0] if profile.data else {"username": uname, "profile_pic_url": "", "bio": "", "id": uid}

        with st.container():
            col1, col2 = st.columns([1, 6])
            with col1:
                st.image(pdata.get("profile_pic_url") or "../assets/def_pfp.png", width=64)
            with col2:
                link = f"[**@{pdata.get('username')}**](https://magicals.streamlit.app/community.py/{pdata.get('username')})"
                st.markdown(f"### {title}")
                st.markdown(f"{link}  n_{pdata.get('bio','')}_")
                st.markdown(desc)
            st.video(e["path"])

            user = st.session_state.get("user")
            like_key = f"like_{e['path']}"
            if like_key not in st.session_state:
                st.session_state[like_key] = False

            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button(f"❤️ {likes}", key=e["path"]):
                    if not user:
                        st.warning("login to like")
                    else:
                        if not st.session_state[like_key]:
                            m["likes"] = likes + 1
                            st.session_state[like_key] = True
                            with open(e["path"].replace(".mp4", ".json"), "w") as fh:
                                json.dump(m, fh)
                            try:
                                supabase.table("magicals").update({"likes": m["likes"]}).eq("path", e["path"]).execute()
                            except:
                                pass
                            st.rerun()
                        else:
                            st.info("already liked")
            with c2:
                if st.button("report", key="r_" + e["path"]):
                    supabase.table("reports").insert({
                        "path": e["path"],
                        "reported_by": st.session_state.get('user', {}).get('email'),
                        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
                    }).execute()
                    st.success("reported")

            st.markdown("---")
            