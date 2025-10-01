from __future__ import annotations
import streamlit as st
from ..state import K


def render() -> None:
    st.subheader("🧾 Basic Information")
    colA, colB = st.columns(2)
    with colA:
        st.text_input("Full Name", key=K["name"])
        st.caption("Example: Tamer Hamad Faour")

        st.text_input("Phone", key=K["phone"])
        st.caption("Example: +49 …")

        st.text_input("GitHub", key=K["github"])
        st.caption("Example: TamerOnLine or https://github.com/TamerOnLine")

        st.text_input("LinkedIn", key=K["linkedin"])
        st.caption("Example: linkedin.com/in/…")

    with colB:
        st.text_input("Location", key=K["location"])
        st.caption("Example: Wuppertal, Germany")

        st.text_input("Email", key=K["email"])
        st.caption("Example: you@example.com")

        st.text_input("Birthdate", key=K["birthdate"])
        st.caption("Example: 01.01.1990")

    st.text_input("Skills (comma separated)", key=K["skills"])
    st.caption("Example: FastAPI, PostgreSQL, Alembic, Docker")

    st.text_input("Languages (comma separated)", key=K["languages"])
    st.caption("Example: Arabic (Native), German (B1), English (B2)")

    st.subheader("📚 Section Texts (Right/Left Columns)")
    st.caption("Use empty lines to separate blocks/items.")

    st.text_area("Projects (raw text block format)", key=K["projects_text"], height=140)
    st.caption("Example:\nNeuroServe\nFastAPI GPU-ready inference server…\nhttps://github.com/…\n\nRepoSmith\nBootstraps Python projects…\nhttps://github.com/…")

    st.text_area("Education (blocks separated by empty lines)", key=K["education_text"], height=120)
    st.caption("Example:\nAI (KI) Development – Mystro GmbH (Wuppertal)\n18.06.2024–30.12.2024 — 1000 hrs\n\nInternship – Yolo GmbH (Wuppertal)\n17.02.2025–14.03.2025")

    st.text_area("Left Column Sections [Title] + - items", key=K["sections_left_text"], height=120)
    st.caption("Example:\n[Certificates]\n- AWS Cloud Practitioner\n- Scrum Basics\n\n[Hobbies]\n- Running\n- Reading")

    st.text_area("Right Column Sections [Title] + - items / paragraphs", key=K["sections_right_text"], height=120)
    st.caption("Example:\n[Profile]\n- Backend developer focused on FastAPI…\n- Experience with LLMs (RAG/Agents)…")

    st.checkbox("Enable RTL for right-side texts (Arabic)", key=K["rtl_mode"])
