from __future__ import annotations

import base64
import json
import mimetypes
import os
from pathlib import Path
import streamlit as st

PHOTO_BYTES_KEY = "photo_bytes"
PHOTO_MIME_KEY = "photo_mime"
PHOTO_NAME_KEY = "photo_name"


def persist_json_atomic(path: Path, data: dict) -> None:
    """Write JSON data to disk atomically using a temporary file."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def guess_mime_from_name(name: str | None) -> str:
    """Guess MIME type based on file name or default to image/png."""
    mt, _ = mimetypes.guess_type(name or "")
    return mt or "image/png"


def encode_photo_to_b64() -> tuple[str | None, str | None, str | None]:
    """Encode uploaded photo to base64 string along with MIME and filename."""
    b = st.session_state.get(PHOTO_BYTES_KEY)
    if not b:
        return None, None, None
    return (
        base64.b64encode(b).decode("utf-8"),
        st.session_state.get(PHOTO_MIME_KEY) or "image/png",
        st.session_state.get(PHOTO_NAME_KEY) or "photo.png",
    )


def decode_photo_from_b64(photo_b64: str, mime: str, name: str) -> None:
    """Decode base64 photo and update session state."""
    try:
        raw = base64.b64decode(photo_b64)
        st.session_state[PHOTO_BYTES_KEY] = raw
        st.session_state[PHOTO_MIME_KEY] = mime or "image/png"
        st.session_state[PHOTO_NAME_KEY] = name or "photo.png"
    except Exception:
        st.session_state[PHOTO_BYTES_KEY] = None
