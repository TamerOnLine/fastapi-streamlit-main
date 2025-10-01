from __future__ import annotations
import streamlit as st
from ..utils import PHOTO_BYTES_KEY, PHOTO_MIME_KEY, PHOTO_NAME_KEY, guess_mime_from_name

def render() -> None:
    st.subheader("📷 صورة شخصية (اختياري)")
    up = st.file_uploader("ارفع صورة (PNG/JPG)", type=["png", "jpg", "jpeg"], accept_multiple_files=False, key="photo_uploader")
    col1, col2 = st.columns([1, 3])
    with col1:
        if up is not None:
            st.session_state[PHOTO_BYTES_KEY] = up.read()
            st.session_state[PHOTO_NAME_KEY] = up.name
            st.session_state[PHOTO_MIME_KEY] = up.type or guess_mime_from_name(up.name)
        if st.session_state.get(PHOTO_BYTES_KEY):
            st.image(st.session_state[PHOTO_BYTES_KEY], caption=st.session_state.get(PHOTO_NAME_KEY) or "photo", width=128)
        else:
            st.caption("لا توجد صورة حالياً.")
    with col2:
        if st.session_state.get(PHOTO_BYTES_KEY):
            if st.button("🧹 إزالة الصورة"):
                st.session_state[PHOTO_BYTES_KEY] = None
                st.session_state[PHOTO_MIME_KEY] = None
                st.session_state[PHOTO_NAME_KEY] = None
                st.rerun()
