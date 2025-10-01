"""
Client-side handler for submitting resume form data to the backend PDF generation API.
"""

from __future__ import annotations

import requests
import streamlit as st

from .utils import PHOTO_BYTES_KEY, PHOTO_NAME_KEY, PHOTO_MIME_KEY


def call_generate_form(api_base: str, form_state: dict) -> bytes:
    """
    Sends resume form data to the FastAPI backend and returns the generated PDF.

    Args:
        api_base (str): Base URL of the backend API.
        form_state (dict): Dictionary containing all form fields and their values.

    Returns:
        bytes: PDF content as bytes.
    """
    url = api_base.rstrip("/") + "/generate-form"
    data = {
        "name": form_state.get("name", ""),
        "location": form_state.get("location", ""),
        "phone": form_state.get("phone", ""),
        "email": form_state.get("email", ""),
        "github": form_state.get("github", ""),
        "linkedin": form_state.get("linkedin", ""),
        "birthdate": form_state.get("birthdate", ""),
        "projects_text": form_state.get("projects_text", ""),
        "education_text": form_state.get("education_text", ""),
        "sections_left_text": form_state.get("sections_left_text", ""),
        "sections_right_text": form_state.get("sections_right_text", ""),
        "skills_text": ", ".join(form_state.get("skills", [])),
        "languages_text": ", ".join(form_state.get("languages", [])),
        "rtl_mode": "true" if form_state.get("rtl_mode") else "false",
    }

    files = None
    if st.session_state.get(PHOTO_BYTES_KEY):
        files = {
            "photo": (
                st.session_state.get(PHOTO_NAME_KEY) or "photo.png",
                st.session_state.get(PHOTO_BYTES_KEY),
                st.session_state.get(PHOTO_MIME_KEY) or "image/png",
            )
        }

    resp = requests.post(url, data=data, files=files, timeout=60)
    resp.raise_for_status()
    return resp.content