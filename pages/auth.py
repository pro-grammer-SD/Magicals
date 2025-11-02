import streamlit as st
from utils.supabase_client import supabase
st.title("login / signup")
mode = st.radio("", ["login","signup"], horizontal=True)
email = st.text_input("email")
password = st.text_input("password", type="password")
if st.button(mode):
    if mode == "signup":
        try:
            supabase.auth.sign_up({"email": email, "password": password})
            st.success("account created. verify your email.")
        except Exception as e:
            st.error(str(e))
    else:
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state.user = {"id": user.user.id, "email": user.user.email}
            st.rerun()
        except Exception as e:
            st.error(str(e))
