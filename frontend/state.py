from __future__ import annotations

import os
import streamlit as st

K = {
    "name": "f_name",
    "location": "f_location",
    "phone": "f_phone",
    "email": "f_email",
    "birthdate": "f_birthdate",
    "github": "f_github",
    "linkedin": "f_linkedin",
    "skills": "f_skills",
    "languages": "f_languages",
    "projects_text": "f_projects_text",
    "education_text": "f_education_text",
    "sections_left_text": "f_sections_left_text",
    "sections_right_text": "f_sections_right_text",
    "rtl_mode": "f_rtl_mode",
    "api_base": "f_api_base",
}

DEFAULT_API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def init_state():
    """Initialize Streamlit session_state with default values."""
    for key in K.values():
        if key not in st.session_state:
            if key == K["rtl_mode"]:
                st.session_state[key] = False
            elif key == K["api_base"]:
                st.session_state[key] = DEFAULT_API_BASE
            else:
                st.session_state[key] = ""
