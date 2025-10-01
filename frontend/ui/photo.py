from __future__ import annotations

import streamlit as st

from ..utils import (
    PHOTO_BYTES_KEY,
    PHOTO_MIME_KEY,
    PHOTO_NAME_KEY,
    guess_mime_from_name,
)

def render() -> None:
    """
    Renders the Streamlit UI component for uploading a profile photo.

    This component allows users to upload a profile image (PNG or JPG format).
    It stores the uploaded image's content, name, and MIME type in the session state.

    Notes:
        - Maintains a dynamic key to ensure uploader resets properly.
        - Provides a button to remove the uploaded photo.
    """
    st.subheader("📷 Profile Photo (Optional)")

    # Initialize dynamic uploader key if not already set
    if "photo_uploader_key" not in st.session_state:
        st.session_state["photo_uploader_key"] = 0

    # File uploader with dynamic key
    up = st.file_uploader(
        "Upload an image (PNG/JPG)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=False,
        key=f"photo_uploader_{st.session_state['photo_uploader_key']}",
    )

    col1, col2 = st.columns([1, 3])

    with col1:
        if up is not None:
            st.session_state[PHOTO_BYTES_KEY] = up.read()
            st.session_state[PHOTO_NAME_KEY] = up.name
            st.session_state[PHOTO_MIME_KEY] = up.type or guess_mime_from_name(up.name)

        if st.session_state.get(PHOTO_BYTES_KEY):
            st.image(
                st.session_state[PHOTO_BYTES_KEY],
                caption=st.session_state.get(PHOTO_NAME_KEY) or "photo",
                width=128,
            )
        else:
            st.caption("No image uploaded.")

    with col2:
        if st.session_state.get(PHOTO_BYTES_KEY):
            if st.button("🧹 Remove Photo"):
                # Clear session state data related to the photo
                st.session_state[PHOTO_BYTES_KEY] = None
                st.session_state[PHOTO_MIME_KEY] = None
                st.session_state[PHOTO_NAME_KEY] = None

                # Increment uploader key to reset file uploader
                st.session_state["photo_uploader_key"] += 1

                # Mark the photo as deleted
                st.session_state["__photo_deleted__"] = True

                st.rerun()
