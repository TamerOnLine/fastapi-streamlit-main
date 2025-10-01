from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import Response

from ..pdf_utils import build_resume_pdf
from ..utils.parsers import (
    parse_csv_or_lines, normalize_language_level,
    parse_projects_blocks, parse_education_blocks,
    parse_sections_text,
)

router = APIRouter()

@router.post("/generate-form")
async def generate_form(
    # معلومات أساسية
    name: str = Form(""),
    location: str = Form(""),
    phone: str = Form(""),
    email: str = Form(""),
    github: str = Form(""),
    linkedin: str = Form(""),
    birthdate: str = Form(""),

    # نصوص حرّة من الواجهة
    projects_text: str = Form(""),
    education_text: str = Form(""),
    sections_left_text: str = Form(""),
    sections_right_text: str = Form(""),

    # مهارات ولغات
    skills_text: str = Form(""),
    languages_text: str = Form(""),

    # خيارات
    rtl_mode: str = Form("false"),

    # صورة شخصية (اختياري)
    photo: Optional[UploadFile] = File(None),
):
    # حمّل الصورة (إن وجدت)
    photo_bytes: Optional[bytes] = await photo.read() if photo else None

    # تحويل النصوص لهياكل
    skills = parse_csv_or_lines(skills_text)
    languages = [normalize_language_level(x) for x in parse_csv_or_lines(languages_text)]
    projects = parse_projects_blocks(projects_text)
    education_items = parse_education_blocks(education_text)
    sections_left = parse_sections_text(sections_left_text)
    sections_right = parse_sections_text(sections_right_text)

    # توليد الـ PDF
    pdf = build_resume_pdf(
        name=name,
        location=location,
        phone=phone,
        email=email,
        github=github,
        linkedin=linkedin,
        birthdate=birthdate,
        skills=skills,
        languages=languages,
        projects=projects,
        education_items=education_items,
        photo_bytes=photo_bytes,
        rtl_mode=(rtl_mode.strip().lower() == "true"),
        sections_left=sections_left,
        sections_right=sections_right,
    )

    return Response(content=pdf, media_type="application/pdf")
