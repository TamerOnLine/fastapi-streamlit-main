"""
Streamlit frontend for the Resume PDF Builder.
Supports payload injection and fallback imports when run as a standalone script.
"""

from __future__ import annotations

import streamlit as st

# --------- Relative imports (within package) ---------
try:
    from .state import init_state, K
    from .utils import decode_photo_from_b64, PHOTO_BYTES_KEY, PHOTO_MIME_KEY, PHOTO_NAME_KEY
    from .ui import sidebar, form, photo
# --------- Fallback for script mode ---------
except ImportError:
    import os
    import sys
    CUR = os.path.dirname(__file__)
    PARENT = os.path.abspath(os.path.join(CUR, os.pardir))
    if PARENT not in sys.path:
        sys.path.insert(0, PARENT)
    from frontend.state import init_state, K
    from frontend.utils import decode_photo_from_b64, PHOTO_BYTES_KEY, PHOTO_MIME_KEY, PHOTO_NAME_KEY
    from frontend.ui import sidebar, form, photo

# --------- Streamlit Configuration ---------
st.set_page_config(page_title="Resume PDF Builder", page_icon="🧾", layout="centered")
st.title("🧾 Resume PDF Builder")

init_state()


# --------- Payload Injection ---------
def _apply_payload_to_form(p: dict) -> None:
    """Apply temporary payload to form session state."""
    st.session_state[K["name"]] = p.get("name", "") or ""
    st.session_state[K["location"]] = p.get("location", "") or ""
    st.session_state[K["phone"]] = p.get("phone", "") or ""
    st.session_state[K["email"]] = p.get("email", "") or ""
    st.session_state[K["birthdate"]] = p.get("birthdate", "") or ""
    st.session_state[K["github"]] = p.get("github", "") or ""
    st.session_state[K["linkedin"]] = p.get("linkedin", "") or ""

    def _join_or_passthrough(v):
        if isinstance(v, list):
            return ", ".join([str(x).strip() for x in v if str(x).strip()])
        return str(v or "")

    st.session_state[K["skills"]] = _join_or_passthrough(p.get("skills", ""))
    st.session_state[K["languages"]] = _join_or_passthrough(p.get("languages", ""))

    st.session_state[K["projects_text"]] = p.get("projects_text", "") or ""
    st.session_state[K["education_text"]] = p.get("education_text", "") or ""
    st.session_state[K["sections_left_text"]] = p.get("sections_left_text", "") or ""
    st.session_state[K["sections_right_text"]] = p.get("sections_right_text", "") or ""
    st.session_state[K["rtl_mode"]] = bool(p.get("rtl_mode", False))

    if p.get("photo_b64"):
        decode_photo_from_b64(
            p.get("photo_b64", ""),
            p.get("photo_mime"),
            p.get("photo_name"),
        )
    else:
        st.session_state[PHOTO_BYTES_KEY] = None
        st.session_state[PHOTO_MIME_KEY] = None
        st.session_state[PHOTO_NAME_KEY] = None


# --------- Run Payload Processing ---------
if "_pending_payload" in st.session_state:
    _apply_payload_to_form(st.session_state["_pending_payload"])
    del st.session_state["_pending_payload"]

# --------- Optional Toast ---------
if st.session_state.pop("_show_loaded_toast", False):
    st.sidebar.success("Loaded successfully ✅")

# --------- Draw UI ---------
sidebar.render()
form.render()
photo.render()
