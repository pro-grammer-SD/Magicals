import streamlit as st

def comment_box(comments, add_comment):
    st.subheader("Comments")
    for c in comments:
        st.markdown(f"🗨️ **@{c['user']}**: {c['text']}")
    text = st.text_input("Write a comment...")
    if st.button("Post"):
        if text.strip():
            add_comment(text.strip())
            