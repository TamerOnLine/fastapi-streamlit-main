from __future__ import annotations
import streamlit as st
from ..state import K

def render() -> None:
    st.subheader("🧾 البيانات الأساسية")
    colA, colB = st.columns(2)
    with colA:
        st.text_input("الاسم", key=K["name"], placeholder="Tamer Hamad Faour")
        st.text_input("الهاتف", key=K["phone"], placeholder="+49 …")
        st.text_input("GitHub", key=K["github"], placeholder="TamerOnLine أو https://github.com/TamerOnLine")
        st.text_input("LinkedIn", key=K["linkedin"], placeholder="linkedin.com/in/…")
    with colB:
        st.text_input("الموقع", key=K["location"], placeholder="Wuppertal, Deutschland")
        st.text_input("البريد الإلكتروني", key=K["email"], placeholder="you@example.com")
        st.text_input("تاريخ الميلاد", key=K["birthdate"], placeholder="01.01.1990")

    st.text_input("المهارات (comma separated)", key=K["skills"], placeholder="FastAPI, PostgreSQL, Alembic, Docker")
    st.text_input("اللغات (comma separated)", key=K["languages"], placeholder="العربية (لغة أم), Deutsch (B1), English (B2)")

    st.subheader("📚 نصوص الأقسام (يمين/يسار)")
    st.caption("استخدم أسطر فارغة للفصل بين العناصر/البلوكات.")

    st.text_area("Projects (نص خام بصيغة البلوكات)", key=K["projects_text"], height=140,
        placeholder=("NeuroServe\nFastAPI GPU-ready inference server…\nhttps://github.com/…\n\n"
                     "RepoSmith\nBootstraps Python projects…\nhttps://github.com/…"))
    st.text_area("Education (بلوكات بسطر فارغ بين كل واحد)", key=K["education_text"], height=120,
        placeholder=("AI (KI) Development – Mystro GmbH (Wuppertal)\n18.06.2024–30.12.2024 — 1000 UE\n\n"
                     "Praktikum – Yolo GmbH (Wuppertal)\n17.02.2025–14.03.2025"))
    st.text_area("Left sections [Title] + - items", key=K["sections_left_text"], height=120,
        placeholder=("[Zertifikate]\n- AWS Cloud Practitioner\n- Scrum Basics\n\n"
                     "[Hobbys]\n- Laufen\n- Lesen"))
    st.text_area("Right sections [Title] + - items / paragraphs", key=K["sections_right_text"], height=120,
        placeholder=("[Profil]\n- Backend-Entwickler mit Fokus auf FastAPI…\n- Erfahrung مع LLMs (RAG/Agenten)…"))
    st.checkbox("تفعيل RTL للنصوص اليمنى (العربية)", key=K["rtl_mode"])
