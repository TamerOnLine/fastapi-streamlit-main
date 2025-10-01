"""
Rendering logic for the left column of the resume, including personal info,
skills, languages, and additional custom sections.
"""

from reportlab.pdfgen import canvas
from reportlab.lib import colors

from .config import *
from .icons import ICON_PATHS, draw_icon_line
from .text import wrap_text, draw_par
from .social import extract_social_handle



def info_line(c, x, y, key: str, value: str, max_w: float, line_gap=LEFT_LINE_GAP, size=LEFT_TEXT_SIZE):
    """
    Draws a single line of text with an optional icon and clickable hyperlink for specific keys.

    Args:
        c: Canvas or drawing context.
        x (float): X-coordinate for the starting point.
        y (float): Y-coordinate for the starting point.
        key (str): Label key (e.g., "GitHub", "LinkedIn", "Phone").
        value (str): Raw input string to be processed.
        max_w (float): Maximum allowed width for the rendered line.
        line_gap (float, optional): Line spacing. Defaults to LEFT_LINE_GAP.
        size (float, optional): Font size. Defaults to LEFT_TEXT_SIZE.

    Returns:
        Rendered line with optional link and icon, if applicable.

    Notes:
        - Only GitHub and LinkedIn values are transformed into clickable links.
        - Non-social fields are rendered as plain text.
    """
    icon = ICON_PATHS.get(key)
    raw = (value or "").strip()
    display = raw
    link = None

    # Only transform social media fields into links
    if key in ("GitHub", "LinkedIn"):
        got = extract_social_handle(key, raw)
        if got:
            display, link = got
        else:
            import re
            v = raw.lower().strip()

            # Remove leading identifiers like 'github:' or 'linkedin:'
            for pref in ("github:", "linkedin:"):
                if v.startswith(pref):
                    v = v[len(pref):].strip()
                    break

            # Clean URL prefixes
            v = re.sub(r'^(https?://)?(www\.)?', '', v, flags=re.I).strip()
            v = v.lstrip('@').strip()

            if key == "GitHub":
                if v.startswith("github.com/"):
                    v = v.split("/", 1)[1]
                v = v.split("/")[0]
                if v:
                    display = v
                    link = f"https://github.com/{v}"

            elif key == "LinkedIn":
                if v.startswith("linkedin.com/"):
                    parts = v.split("/", 2)
                    if len(parts) >= 3:
                        v = parts[2]
                v = v.split("/")[0]
                if v:
                    display = v
                    link = f"https://www.linkedin.com/in/{v}"

    return draw_icon_line(
        c, x, y, icon, display,
        icon_w=ICON_SIZE, icon_h=ICON_SIZE, pad_x=ICON_PAD_X, size=size,
        line_gap=line_gap, max_w=max_w, link_url=link
    )


def draw_left_extra_sections(
    c: canvas.Canvas,
    inner_x: float,
    inner_w: float,
    cursor: float,
    sections_left: list[dict]
) -> float:
    """Draws user-defined sections on the left column."""
    for sec in (sections_left or []):
        title = (sec.get("title") or "").strip()
        lines = [str(x).strip() for x in (sec.get("lines") or []) if str(x).strip()]
        if not title or not lines:
            continue
        cursor -= LEFT_SEC_TITLE_TOP_GAP
        c.setFont("Helvetica-Bold", LEFT_SEC_HEADING_SIZE)
        c.setFillColor(colors.black)
        if LEFT_SEC_TITLE_ALIGN == "center":
            c.drawCentredString(inner_x + inner_w / 2, cursor, title)
        elif LEFT_SEC_TITLE_ALIGN == "right":
            c.drawRightString(inner_x + inner_w, cursor, title)
        else:
            c.drawString(inner_x, cursor, title)
        cursor -= LEFT_SEC_TITLE_BOTTOM_GAP
        c.setStrokeColor(LEFT_SEC_RULE_COLOR)
        c.setLineWidth(LEFT_SEC_RULE_WIDTH)
        c.line(inner_x, cursor, inner_x + inner_w, cursor)
        cursor -= LEFT_SEC_RULE_TO_LIST_GAP
        c.setFont("Helvetica", LEFT_SEC_TEXT_SIZE)
        c.setFillColor(colors.black)
        for ln in lines:
            c.circle(inner_x + LEFT_SEC_BULLET_X_OFFSET, cursor + 3, LEFT_SEC_BULLET_RADIUS, stroke=1, fill=1)
            c.drawString(inner_x + LEFT_SEC_TEXT_X_OFFSET, cursor, ln)
            cursor -= LEFT_SEC_LINE_GAP
        cursor -= LEFT_SEC_SECTION_GAP
    return cursor


def draw_left_column(
    c: canvas.Canvas,
    *,
    name: str,
    location: str,
    phone: str,
    email: str,
    github: str,
    linkedin: str,
    birthdate: str,
    skills: list[str],
    languages: list[str],
    inner_x: float,
    inner_w: float,
    cursor: float,
) -> float:
    """Draws the full left column including contact, skills, and language sections."""
    if name:
        c.setFont("Helvetica-Bold", NAME_SIZE)
        c.setFillColor(HEADING_COLOR)
        c.drawCentredString(inner_x + inner_w / 2, cursor, name)
        cursor -= NAME_GAP

    has_contact = any([location, phone, email, birthdate, github, linkedin])
    if has_contact:
        c.setFont("Helvetica-Bold", HEADING_SIZE)
        c.setFillColor(HEADING_COLOR)
        c.drawCentredString(inner_x + inner_w / 2, cursor, "Pers\u00f6nliche Informationen")
        cursor -= 6
        from .shapes import draw_rule
        draw_rule(c, inner_x, cursor, inner_w)
        cursor -= 6

        if location:
            cursor = info_line(c, inner_x, cursor, "Ort", location, inner_w)
        if phone:
            cursor = info_line(c, inner_x, cursor, "Telefon", phone, inner_w)
        if email:
            cursor = info_line(c, inner_x, cursor, "E-Mail", email, inner_w)
        if birthdate:
            cursor = info_line(c, inner_x, cursor, "Geburtsdatum", birthdate, inner_w)
        if github:
            cursor = info_line(c, inner_x, cursor, "GitHub", github, inner_w)
        if linkedin:
            cursor = info_line(c, inner_x, cursor, "LinkedIn", linkedin, inner_w)

        cursor -= LEFT_AFTER_CONTACT_GAP

    if skills:
        cursor -= LEFT_SEC_TITLE_TOP_GAP
        c.setFont("Helvetica-Bold", LEFT_SEC_HEADING_SIZE)
        c.setFillColor(HEADING_COLOR)
        if LEFT_SEC_TITLE_ALIGN == "center":
            c.drawCentredString(inner_x + inner_w / 2, cursor, "Technische F\u00e4higkeiten")
        elif LEFT_SEC_TITLE_ALIGN == "right":
            c.drawRightString(inner_x + inner_w, cursor, "Technische F\u00e4higkeiten")
        else:
            c.drawString(inner_x, cursor, "Technische F\u00e4higkeiten")
        cursor -= LEFT_SEC_TITLE_BOTTOM_GAP
        c.setStrokeColor(LEFT_SEC_RULE_COLOR)
        c.setLineWidth(LEFT_SEC_RULE_WIDTH)
        c.line(inner_x, cursor, inner_x + inner_w, cursor)
        cursor -= LEFT_SEC_RULE_TO_LIST_GAP
        c.setFont("Helvetica", LEFT_SEC_TEXT_SIZE)
        c.setFillColor(colors.black)
        max_text_w = inner_w - (LEFT_SEC_TEXT_X_OFFSET + 2)
        for sk in skills:
            wrapped = wrap_text(sk, "Helvetica", LEFT_SEC_TEXT_SIZE, max_text_w)
            for i, ln in enumerate(wrapped):
                if i == 0:
                    c.circle(inner_x + LEFT_SEC_BULLET_X_OFFSET, cursor + 3, LEFT_SEC_BULLET_RADIUS, stroke=1, fill=1)
                c.drawString(inner_x + LEFT_SEC_TEXT_X_OFFSET, cursor, ln)
                cursor -= LEFT_SEC_LINE_GAP
        cursor -= LEFT_SEC_SECTION_GAP

    if languages:
        cursor -= LEFT_SEC_TITLE_TOP_GAP
        c.setFont("Helvetica-Bold", LEFT_SEC_HEADING_SIZE)
        if LEFT_SEC_TITLE_ALIGN == "center":
            c.drawCentredString(inner_x + inner_w / 2, cursor, "Sprachen")
        elif LEFT_SEC_TITLE_ALIGN == "right":
            c.drawRightString(inner_x + inner_w, cursor, "Sprachen")
        else:
            c.drawString(inner_x, cursor, "Sprachen")
        cursor -= LEFT_SEC_TITLE_BOTTOM_GAP
        c.setStrokeColor(LEFT_SEC_RULE_COLOR)
        c.setLineWidth(LEFT_SEC_RULE_WIDTH)
        c.line(inner_x, cursor, inner_x + inner_w, cursor)
        cursor -= LEFT_SEC_RULE_TO_LIST_GAP
        c.setFont("Helvetica", LEFT_SEC_TEXT_SIZE)
        langs = ", ".join(languages)
        cursor = draw_par(
            c, inner_x, cursor, [langs], "Helvetica", LEFT_SEC_TEXT_SIZE,
            inner_w, "left", False, LEFT_SEC_LINE_GAP
        )
        cursor -= LEFT_SEC_SECTION_GAP

    return cursor