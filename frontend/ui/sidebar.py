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
        "name": st.session_state.get(K["name"], "") or "",
        "location": st.session_state.get(K["location"], "") or "",
        "phone": st.session_state.get(K["phone"], "") or "",
        "email": st.session_state.get(K["email"], "") or "",
        "github": st.session_state.get(K["github"], "") or "",
        "linkedin": st.session_state.get(K["linkedin"], "") or "",
        "birthdate": st.session_state.get(K["birthdate"], "") or "",
        "skills": _split_by_comma(st.session_state.get(K["skills"], "")),
        "languages": _split_by_comma(st.session_state.get(K["languages"], "")),
        "projects_text": st.session_state.get(K["projects_text"], "") or "",
        "education_text": st.session_state.get(K["education_text"], "") or "",
        "sections_left_text": st.session_state.get(K["sections_left_text"], "") or "",
        "sections_right_text": st.session_state.get(K["sections_right_text"], "") or "",
        "rtl_mode": bool(st.session_state.get(K["rtl_mode"], False)),
    }
    photo_b64, photo_mime, photo_name = encode_photo_to_b64()
    payload.update({"photo_b64": photo_b64, "photo_mime": photo_mime, "photo_name": photo_name})
    return payload

def _apply_payload_to_form(p: Dict[str, Any]) -> None:
    st.session_state[K["name"]] = p.get("name", "") or ""
    st.session_state[K["location"]] = p.get("location", "") or ""
    st.session_state[K["phone"]] = p.get("phone", "") or ""
    st.session_state[K["email"]] = p.get("email", "") or ""
    st.session_state[K["birthdate"]] = p.get("birthdate", "") or ""
    st.session_state[K["github"]] = p.get("github", "") or ""
    st.session_state[K["linkedin"]] = p.get("linkedin", "") or ""
    st.session_state[K["skills"]] = _join_or_passthrough(p.get("skills", ""))
    st.session_state[K["languages"]] = _join_or_passthrough(p.get("languages", ""))
    st.session_state[K["projects_text"]] = p.get("projects_text", "") or ""
    st.session_state[K["education_text"]] = p.get("education_text", "") or ""
    st.session_state[K["sections_left_text"]] = p.get("sections_left_text", "") or ""
    st.session_state[K["sections_right_text"]] = p.get("sections_right_text", "") or ""
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
    if "pdf_bytes" not in st.session_state: st.session_state.pdf_bytes = None
    if "pdf_filename" not in st.session_state: st.session_state.pdf_filename = "resume.pdf"

    st.sidebar.subheader("API connection")
    st.sidebar.text_input("API Base URL", key=K["api_base"],
                          help="مثال: http://127.0.0.1:8000 أو http://localhost:8000",
                          placeholder=DEFAULT_API_BASE)

    st.sidebar.header("💾 Save / Load (مع الصورة)")
    preset_name = st.sidebar.text_input("Preset name", value="", placeholder="my-profile")

    # داخل render() في sidebar.py

    uploaded_json = st.sidebar.file_uploader("Browse JSON (Load)", type=["json"], key="json_loader")
    if st.sidebar.button("Load uploaded"):
        if uploaded_json is None:
            st.sidebar.warning("اختر ملف JSON أولاً.")
        else:
            try:
                content = json.loads(uploaded_json.read().decode("utf-8"))
                # لا نعدّل مفاتيح widgets الآن — نحفظ مؤقتاً ونُعيد التشغيل
                st.session_state["_pending_payload"] = content
                st.session_state["_show_loaded_toast"] = True
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"فشل التحميل: {e}")


    if st.sidebar.button("Save current"):
        if not preset_name.strip():
            st.sidebar.warning("اكتب اسم Preset.")
        else:
            out = PROFILES_DIR / f"{preset_name.strip()}.json"
            try:
                persist_json_atomic(out, _payload_from_form())
                st.sidebar.success(f"تم الحفظ: {out.name}")
            except Exception as e:
                st.sidebar.error(f"فشل الحفظ: {e}")

    st.sidebar.header("📄 PDF Generator")
    if st.sidebar.button("🧾 Generate PDF"):
        try:
            pdf_bytes = call_generate_form(_api_base_value(), _payload_from_form())
            st.session_state.pdf_bytes = pdf_bytes
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state.pdf_filename = f"resume_{ts}.pdf"
            st.sidebar.success("تم إنشاء الـ PDF ✅")
        except Exception as e:
            st.sidebar.error(f"فشل طلب التوليد: {e}")

    if st.session_state.get("pdf_bytes"):
        st.sidebar.download_button("⬇️ Download PDF",
                                   data=st.session_state.pdf_bytes,
                                   file_name=st.session_state.pdf_filename,
                                   mime="application/pdf")
