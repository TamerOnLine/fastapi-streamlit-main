from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime
import json
import streamlit as st

from ..state import K, DEFAULT_API_BASE
from ..api_client import call_generate_form
from ..utils import (
    persist_json_atomic, encode_photo_to_b64, decode_photo_from_b64,
    PHOTO_BYTES_KEY, PHOTO_MIME_KEY, PHOTO_NAME_KEY,
)

BASE_DIR = Path(__file__).resolve().parents[2]
PROFILES_DIR = BASE_DIR / "profiles"
OUTPUTS_DIR = BASE_DIR / "outputs"
PROFILES_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

def _payload_from_form() -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "name": st.session_state.get(K["name"], ""),
        "location": st.session_state.get(K["location"], ""),
        "phone": st.session_state.get(K["phone"], ""),
        "email": st.session_state.get(K["email"], ""),
        "github": st.session_state.get(K["github"], ""),
        "linkedin": st.session_state.get(K["linkedin"], ""),
        "birthdate": st.session_state.get(K["birthdate"], ""),
        "skills": _split_by_comma(st.session_state.get(K["skills"], "")),
        "languages": _split_by_comma(st.session_state.get(K["languages"], "")),
        "projects_text": st.session_state.get(K["projects_text"], ""),
        "education_text": st.session_state.get(K["education_text"], ""),
        "sections_left_text": st.session_state.get(K["sections_left_text"], ""),
        "sections_right_text": st.session_state.get(K["sections_right_text"], ""),
        "rtl_mode": bool(st.session_state.get(K["rtl_mode"], False)),
    }
    photo_b64, photo_mime, photo_name = encode_photo_to_b64()
    payload.update({"photo_b64": photo_b64, "photo_mime": photo_mime, "photo_name": photo_name})
    return payload

def _apply_payload_to_form(p: Dict[str, Any]) -> None:
    st.session_state[K["name"]] = p.get("name", "")
    st.session_state[K["location"]] = p.get("location", "")
    st.session_state[K["phone"]] = p.get("phone", "")
    st.session_state[K["email"]] = p.get("email", "")
    st.session_state[K["birthdate"]] = p.get("birthdate", "")
    st.session_state[K["github"]] = p.get("github", "")
    st.session_state[K["linkedin"]] = p.get("linkedin", "")
    st.session_state[K["skills"]] = _join_or_passthrough(p.get("skills", ""))
    st.session_state[K["languages"]] = _join_or_passthrough(p.get("languages", ""))
    st.session_state[K["projects_text"]] = p.get("projects_text", "")
    st.session_state[K["education_text"]] = p.get("education_text", "")
    st.session_state[K["sections_left_text"]] = p.get("sections_left_text", "")
    st.session_state[K["sections_right_text"]] = p.get("sections_right_text", "")
    st.session_state[K["rtl_mode"]] = bool(p.get("rtl_mode", False))
    if p.get("photo_b64"):
        decode_photo_from_b64(p.get("photo_b64", ""), p.get("photo_mime"), p.get("photo_name"))
    else:
        st.session_state[PHOTO_BYTES_KEY] = None
        st.session_state[PHOTO_MIME_KEY] = None
        st.session_state[PHOTO_NAME_KEY] = None

def _split_by_comma(s: Any) -> List[str]:
    if not isinstance(s, str): return list(s or [])
    return [part.strip() for part in s.split(",") if part.strip()]

def _join_or_passthrough(v: Any) -> str:
    if isinstance(v, list): return ", ".join([str(x).strip() for x in v if str(x).strip()])
    return str(v or "")

def _api_base_value() -> str:
    base = (st.session_state.get(K["api_base"]) or "").strip()
    if not base:
        base = DEFAULT_API_BASE
        st.session_state[K["api_base"]] = DEFAULT_API_BASE
    return base.rstrip("/")

def render() -> None:
    if "pdf_bytes" not in st.session_state:
        st.session_state.pdf_bytes = None
    if "pdf_filename" not in st.session_state:
        st.session_state.pdf_filename = "resume.pdf"

    st.sidebar.subheader("API Connection")
    st.sidebar.text_input("API Base URL", key=K["api_base"],
                          help="Example: http://127.0.0.1:8000 or http://localhost:8000",
                          placeholder=DEFAULT_API_BASE)

    st.sidebar.header("💾 Save / Load (includes photo)")
    preset_name = st.sidebar.text_input("Preset Name", value="", placeholder="my-profile")

    uploaded_json = st.sidebar.file_uploader("Browse JSON (Load)", type=["json"], key="json_loader")
    if st.sidebar.button("Load uploaded"):
        if uploaded_json is None:
            st.sidebar.warning("Please select a JSON file first.")
        else:
            try:
                content = json.loads(uploaded_json.read().decode("utf-8"))
                st.session_state["_pending_payload"] = content
                st.session_state["_show_loaded_toast"] = True
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Failed to load: {e}")

    if st.sidebar.button("Save current"):
        if not preset_name.strip():
            st.sidebar.warning("Please enter a preset name.")
        else:
            out = PROFILES_DIR / f"{preset_name.strip()}.json"
            try:
                persist_json_atomic(out, _payload_from_form())
                st.sidebar.success(f"Saved successfully: {out.name}")
            except Exception as e:
                st.sidebar.error(f"Failed to save: {e}")

    st.sidebar.header("📄 PDF Generator")
    if st.sidebar.button("🧾 Generate PDF"):
        try:
            pdf_bytes = call_generate_form(_api_base_value(), _payload_from_form())
            st.session_state.pdf_bytes = pdf_bytes
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state.pdf_filename = f"resume_{ts}.pdf"
            st.sidebar.success("PDF generated successfully ✅")
        except Exception as e:
            st.sidebar.error(f"Generation request failed: {e}")

    if st.session_state.get("pdf_bytes"):
        st.sidebar.download_button("⬇️ Download PDF",
                                   data=st.session_state.pdf_bytes,
                                   file_name=st.session_state.pdf_filename,
                                   mime="application/pdf")
