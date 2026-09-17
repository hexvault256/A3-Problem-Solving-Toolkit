#!/usr/bin/env python3
"""
build_a3.py — Generate a one-page A3 problem-solving report (.pptx) that matches
the reference format exactly: 14x10.5" landscape, two columns, numbered black
section-header bars, white bordered content boxes, a Five-Whys flowchart drawn
with red "Why-N" labels + blue curved/branch arrows, a cost table, and a
timeline table.

Usage:
    python build_a3.py spec.json output.pptx

The spec is a JSON file. See references/spec_schema.md for the full schema and
a3_format.md for the design rationale. A minimal spec only needs `meta.title`;
every section is optional and is simply skipped (with its grid slot left blank)
if absent — but a complete A3 has all 8 sections.

Design intent: this script owns the *format* so every invocation looks the same.
The model's job is to produce good *content* in the JSON spec; the layout, fonts,
colors, arrows, and tables are handled here so they never drift from the
reference. Keep font sizes >= 10 pt (human-centered readability requirement).
"""

import json
import sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn

# ---------------------------------------------------------------------------
# Palette (matches the reference theme)
# ---------------------------------------------------------------------------
BLACK = RGBColor(0x00, 0x00, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED   = RGBColor(0xFF, 0x00, 0x00)
BLUE  = RGBColor(0x2E, 0x5B, 0xA8)   # accent1-like, for flowchart text/labels
ARROW_BLUE = RGBColor(0x44, 0x72, 0xC4)  # Office accent1 blue (arrow fill)
GRAY_HEADER = RGBColor(0xD9, 0xD9, 0xD9)  # table header / total row fill

# ---------------------------------------------------------------------------
# Page + grid geometry (inches) — derived from the reference slide
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = 14.0, 10.5

# Two columns
LCOL_X, COL_W = 0.20, 6.53
RCOL_X = 7.24

HDR_H = 0.40          # section header bar height
GAP   = 0.02          # gap between header bar and its content box

# Fixed typography. Body text is one uniform size everywhere; section header bars
# are larger. We deliberately do NOT auto-shrink to fit — if content overflows,
# the fix is to rewrite (shorten) the content, not to shrink the font. The
# builder warns on stderr when a section is likely to overflow so the author
# knows to trim. (Tables are data grids and keep their own smaller size.)
BODY_PT   = 13        # all body text (bullets, blocks, cost bullets)
HEADER_PT = 16        # section header bars + identity lines
FLOW_PT   = 12        # everything inside the Five-Whys flowchart
TITLE_PT  = 20        # the one document title at the very top


# ===========================================================================
# Low-level drawing helpers
# ===========================================================================
def _set_fill(shape, rgb):
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb


def _set_line(shape, rgb, width_pt=1.0):
    shape.line.color.rgb = rgb
    shape.line.width = Pt(width_pt)


def _no_line(shape):
    shape.line.fill.background()


def section_header(slide, x, y, w, text):
    """Black bar with white text, e.g. '1. Background'."""
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                 Inches(w), Inches(HDR_H))
    _set_fill(box, BLACK)
    _set_line(box, BLACK, 1.0)
    box.shadow.inherit = False
    tf = box.text_frame
    tf.margin_top = Pt(1); tf.margin_bottom = Pt(1)
    tf.margin_left = Pt(6); tf.margin_right = Pt(6)
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = text
    r.font.size = Pt(16); r.font.bold = False; r.font.color.rgb = WHITE
    return box


def content_box(slide, x, y, w, h):
    """White rectangle with a thin black outline."""
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                 Inches(w), Inches(h))
    _set_fill(box, WHITE)
    _set_line(box, BLACK, 1.0)
    box.shadow.inherit = False
    tf = box.text_frame
    tf.word_wrap = True
    # Safety valve: if content slightly exceeds the (fixed, reference-matching)
    # box, let PowerPoint shrink the text to fit rather than clip it. Keep
    # content lean so this rarely triggers — readability still wants >=10 pt.
    tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    tf.margin_left = Pt(7); tf.margin_right = Pt(7)
    tf.margin_top = Pt(4); tf.margin_bottom = Pt(4)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    return box


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Pt(2); tf.margin_right = Pt(2)
    tf.margin_top = Pt(1); tf.margin_bottom = Pt(1)
    tf.vertical_anchor = anchor
    return tb


def _para_compact(p, mar_l_in=0.0, hanging_in=0.0, line_spacing=1.0):
    """Tighten a paragraph: remove the default before/after spacing (so dense
    sections fit without clipping) and control the left margin / hanging indent
    (so bulleted sub-points sit close to the left edge instead of far indented)."""
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    p.line_spacing = line_spacing
    pPr = p._p.get_or_add_pPr()
    pPr.set('marL', str(int(mar_l_in * 914400)))
    pPr.set('indent', str(int(-hanging_in * 914400)))


def _add_run(p, text, size, bold=False, color=None):
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    # Shapes created via add_shape default their font to the theme's
    # on-accent color (often white), so always set an explicit color. Black is
    # the safe default for body text on the white content boxes.
    r.font.color.rgb = color if color is not None else BLACK
    return r


# Roman numerals / letters for list markers
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV"]


def _marker(style, i):
    if style == "roman":
        return f"{ROMAN[i]}. " if i < len(ROMAN) else f"{i+1}. "
    if style == "alpha-lower":
        return f"{chr(ord('a') + i)}) "
    if style == "alpha-upper":
        return f"{chr(ord('A') + i)}. "
    if style == "number":
        return f"{i+1}. "
    if style == "none":
        return ""
    return "•  "  # bullet default


def fill_list(text_frame, items, style="bullet", size=14, color=None,
              clear=True):
    """Write a list of strings into a text frame with markers."""
    if clear:
        text_frame.clear()
    first = True
    for i, item in enumerate(items):
        # Each item may be a dict {"text":..., "color":..., "bold":...}
        if isinstance(item, dict):
            txt = item.get("text", "")
            label = item.get("label")  # rendered bold before the text
            c = _parse_color(item.get("color")) if item.get("color") else color
            bold = item.get("bold", False)
        else:
            txt, c, bold, label = str(item), color, False, None
        p = text_frame.paragraphs[0] if first else text_frame.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.LEFT  # autoshape first paragraph defaults center
        _para_compact(p)
        _add_run(p, _marker(style, i), size, bold=bold, color=c)
        if label:
            _add_run(p, label + "：", size, bold=True, color=c)
        _add_run(p, txt, size, bold=bold, color=c)


def _char_width_units(ch):
    """Approx character advance width in 'em' units relative to font size.
    CJK / full-width characters are ~1.0 em; Latin/space ~0.5 em."""
    o = ord(ch)
    if (0x3000 <= o <= 0x9FFF or 0xFF00 <= o <= 0xFFEF or
            0x3040 <= o <= 0x30FF or 0x4E00 <= o <= 0x9FFF):
        return 1.0   # CJK punctuation, kana, kanji, full-width forms
    return 0.5


def _est_lines(text, width_in, size_pt):
    """Estimate wrapped lines for `text` in a box `width_in` wide at `size_pt`,
    accounting for full-width (Japanese) vs half-width (Latin) characters. One
    line holds (width_in*72 / size_pt) em-units of advance width."""
    line_units = max(4.0, (width_in * 72.0) / size_pt)
    n = 0
    for line in str(text).split("\n"):
        units = sum(_char_width_units(c) for c in line)
        n += max(1, -(-int(units * 100) // int(line_units * 100)))  # ceil
    return n


def fit_size(texts, width_in, height_in, max_size=14, min_size=10,
             line_factor=1.22, extra_lines=0):
    """Largest font size in [min,max] at which `texts` (a list of strings) fits
    in a box of the given height. (Kept for callers that still want it; the main
    sections now use fixed sizes instead — see BODY_PT / FLOW_PT.)"""
    usable_h = height_in - 0.10  # top+bottom margins
    for size in range(int(max_size), int(min_size) - 1, -1):
        lines = extra_lines + sum(_est_lines(t, width_in - 0.18, size)
                                  for t in texts)
        if lines * (size * line_factor / 72.0) <= usable_h:
            return size
    return min_size


def warn_overflow(name, texts, width_in, height_in, size, extra_lines=0):
    """Estimate whether `texts` fit in the box at the fixed `size`; if not, print
    a stderr warning telling the author to shorten the content (we never shrink
    the font for these sections). Returns the estimated overflow in lines."""
    lines = extra_lines + sum(_est_lines(t, width_in - 0.20, size)
                              for t in texts)
    capacity = max(1, (height_in - 0.10) / (size * 1.18 / 72.0))
    if lines > capacity + 0.4:
        sys.stderr.write(
            f"[overflow] section '{name}': ~{lines} lines of text but only "
            f"~{int(capacity)} fit at {size}pt. Shorten the content (do not "
            f"rely on shrinking).\n")
    return lines - capacity


def _parse_color(val):
    if val is None:
        return None
    if isinstance(val, str):
        v = val.strip().lstrip("#")
        named = {"red": "FF0000", "blue": "2E5BA8", "black": "000000",
                 "white": "FFFFFF", "green": "008000"}
        v = named.get(val.strip().lower(), v)
        return RGBColor.from_string(v.upper())
    return None


# ===========================================================================
# Arrows for the flowchart
# ===========================================================================
def curved_down_arrow(slide, x, y, w=0.25, h=0.16):
    """Blue curved-down arrow (the 'same row, next step' connector)."""
    a = slide.shapes.add_shape(MSO_SHAPE.CURVED_DOWN_ARROW, Inches(x),
                               Inches(y), Inches(w), Inches(h))
    a.shadow.inherit = False
    return a  # default theme style is the accent1 blue, matching reference


def branch_arrow(slide, x, y, w=0.45, h=0.10, rotation=35):
    """Blue right-arrow rotated to point diagonally down — used to branch to a
    sub-cause on the row below."""
    a = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y),
                               Inches(w), Inches(h))
    a.rotation = rotation
    a.shadow.inherit = False
    return a


def why_label(slide, center_x, y, text="Why-1"):
    """Red 'Why-N' label, horizontally centered at center_x (placed directly
    above the blue connector arrow it describes)."""
    w = 0.8
    tb = textbox(slide, center_x - w / 2, y, w, 0.20, anchor=MSO_ANCHOR.MIDDLE)
    p = tb.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    _para_compact(p)
    _add_run(p, text, FLOW_PT, bold=False, color=RED)
    return tb


# ===========================================================================
# Section renderers
# ===========================================================================
def render_simple_section(slide, x, y, w, h, num, title, content):
    """Header bar + content box holding a bullet/roman/lettered list, optional
    leading bold-heading blocks, an optional image, and an optional table
    (used by iteration sheets for the previous-round results / Check table)."""
    section_header(slide, x, y, w, f"{num}. {title}")
    box_y = y + HDR_H + GAP
    box = content_box(slide, x, box_y, w, h)
    tf = box.text_frame

    if isinstance(content, dict):
        items = content.get("items", [])
        style = content.get("style", "bullet")
        size = content.get("size", BODY_PT)
        blocks = content.get("blocks")
        image = content.get("image")
        table = content.get("table")
    elif isinstance(content, list):
        items, style, size, blocks, image = content, "bullet", BODY_PT, None, None
        table = None
    else:
        items, style, size, blocks, image = [], "bullet", BODY_PT, None, None
        table = None

    # If a table is present it takes the bottom of the section; the item list
    # gets the remaining height (PowerPoint enforces a per-row minimum tied to
    # the cell font size, so honor that floor or the last rows get clipped).
    items_h = h
    if table:
        nrows = (1 if table.get("headers") else 0) + len(table.get("rows", []))
        tsize = table.get("size", 9)
        floor = tsize / 72.0 + 0.045
        row_h = max(table.get("row_h", 0.16), floor)
        table = dict(table); table["row_h"] = row_h; table["size"] = tsize
        table_h = nrows * row_h
        items_h = max(0.0, h - table_h - 0.10)

    if blocks:
        _render_blocks(tf, blocks, box_w=w, box_h=items_h, name=f"{num}.{title}")
    elif items:
        texts = [it.get("text", "") if isinstance(it, dict) else str(it)
                 for it in items]
        warn_overflow(f"{num}. {title}", texts, w, items_h, size)
        fill_list(tf, items, style=style, size=size)

    if table:
        _add_table(slide, x + 0.05, box_y + items_h + 0.05, w - 0.10, table)

    # Optional image inside / overlapping the box (e.g. the photo in section 2)
    if image:
        try:
            import os
            if os.path.exists(image):
                iw = content.get("image_w", 2.15)
                ih = content.get("image_h", 1.45)
                ix = x + w - iw - 0.10
                iy = box_y + 0.05
                slide.shapes.add_picture(image, Inches(ix), Inches(iy),
                                         Inches(iw), Inches(ih))
        except Exception as e:
            sys.stderr.write(f"[warn] could not add image {image}: {e}\n")
    return box


def _render_blocks(tf, blocks, box_w=6.53, box_h=2.5, name="blocks"):
    """Blocks = list of {heading, points, style, heading_color, point_color}.
    Heading is bold; points are an indented marker list. Used for sections 5/6
    (Deep Analysis / Countermeasures). Body text is a fixed size (BODY_PT); if
    the content overflows, the author should shorten it (we warn on stderr)."""
    tf.clear()
    # Gather all text to estimate overflow at the fixed body size.
    all_texts = []
    for blk in blocks:
        if blk.get("heading") is not None:
            all_texts.append(blk["heading"])
        for pt in blk.get("points", []):
            all_texts.append(pt.get("text", "") if isinstance(pt, dict)
                             else str(pt))
    warn_overflow(name, all_texts, box_w - 0.16, box_h, BODY_PT)
    first = True
    for blk in blocks:
        heading = blk.get("heading")
        points = blk.get("points", [])
        style = blk.get("style", "bullet")
        size = blk.get("size", BODY_PT)
        hcolor = _parse_color(blk.get("heading_color")) or BLACK
        pcolor = _parse_color(blk.get("point_color"))
        if heading is not None:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.alignment = PP_ALIGN.LEFT
            _para_compact(p, mar_l_in=0.0)  # heading flush left
            _add_run(p, heading, size, bold=True, color=hcolor)
        for i, pt in enumerate(points):
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.alignment = PP_ALIGN.LEFT
            # Small hanging indent: marker at the left edge, wrapped lines align
            # just under the text — no large empty left gutter.
            _para_compact(p, mar_l_in=0.16, hanging_in=0.16)
            if isinstance(pt, dict):
                txt = pt.get("text", "")
                c = _parse_color(pt.get("color")) or pcolor
            else:
                txt, c = str(pt), pcolor
            _add_run(p, _marker(style, i), size, color=c)
            _add_run(p, txt, size, color=c)


def render_cost_section(slide, x, y, w, num, title, cost, bottom_limit):
    """Bullets followed by an optional cost table, fitted into the vertical
    space between this header and `bottom_limit` (the next section's header)."""
    section_header(slide, x, y, w, f"{num}. {title}")
    box_y = y + HDR_H + GAP
    bullets = cost.get("bullets", [])
    table = cost.get("table")

    avail = bottom_limit - box_y - 0.06
    # PowerPoint enforces a minimum row height tied to the cell font size, so
    # the table's real footprint is nrows * (font/72 + padding). Account for
    # that floor (otherwise the last rows get clipped) and give the table its
    # needed height first, then let the bullets take the remainder.
    if table:
        nrows = (1 if table.get("headers") else 0) + len(table.get("rows", []))
        tsize = table.get("size", 9)
        floor = tsize / 72.0 + 0.045
        row_h = max(table.get("row_h", 0.16), floor)
        table = dict(table); table["row_h"] = row_h; table["size"] = tsize
        table_h = nrows * row_h
    else:
        table_h = 0.0

    box_h = cost.get("box_h")
    if box_h is None:
        box_h = max(0.45, avail - table_h - (0.06 if table else 0))
    box = content_box(slide, x, box_y, w, box_h)
    if bullets:
        btexts = [(b.get("label", "") + b.get("text", "")) if isinstance(b, dict)
                  else str(b) for b in bullets]
        warn_overflow(f"{num}. {title} (bullets)", btexts, w, box_h, BODY_PT)
        fill_list(box.text_frame, bullets, style="bullet", size=BODY_PT)
    if table:
        _add_table(slide, x, box_y + box_h + 0.06, w, table, borders=True)
    return box


_CELL_LINE_TAGS = ("a:lnL", "a:lnR", "a:lnT", "a:lnB")


def _set_cell_borders(cell, rgb=BLACK, width_pt=0.75):
    """Rule a single table cell on all four sides.

    A python-pptx table inherits a theme table style whose grid lines are
    white, so a table whose cells are filled white/gray renders with no
    visible grid at all. A classic A3 cost table and timeline are ruled, so
    the lines are written explicitly into <a:tcPr> instead of being left to
    the theme.
    """
    tc_pr = cell._tc.get_or_add_tcPr()
    for tag in _CELL_LINE_TAGS:
        for old in tc_pr.findall(qn(tag)):
            tc_pr.remove(old)
    emu = int(Pt(width_pt))
    color = str(rgb)
    # In a:tcPr the line elements must come *before* the fill element, so
    # insert them at the front in reverse order (result: lnL, lnR, lnT, lnB).
    for tag in reversed(_CELL_LINE_TAGS):
        tc_pr.insert(0, parse_xml(
            '<{t} xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
            ' w="{w}" cap="flat" cmpd="sng" algn="ctr">'
            '<a:solidFill><a:srgbClr val="{c}"/></a:solidFill>'
            '<a:prstDash val="solid"/></{t}>'.format(t=tag, w=emu, c=color)))


def _add_table(slide, x, y, w, table, borders=False):
    headers = table.get("headers", [])
    rows = table.get("rows", [])
    highlight_last = table.get("highlight_last", False)
    size = table.get("size", 11)
    ncols = len(headers) if headers else (len(rows[0]) if rows else 1)
    nrows = (1 if headers else 0) + len(rows)
    row_h = table.get("row_h", 0.22)
    h = row_h * nrows
    gtbl = slide.shapes.add_table(nrows, ncols, Inches(x), Inches(y),
                                  Inches(w), Inches(h)).table
    # turn off banded styling for a clean grid
    gtbl.first_row = bool(headers)
    gtbl.horz_banding = False
    r0 = 0
    if headers:
        for c, htext in enumerate(headers):
            cell = gtbl.cell(0, c)
            _fmt_cell(cell, htext, size, bold=True, fill=GRAY_HEADER)
        r0 = 1
    for ri, row in enumerate(rows):
        is_total = highlight_last and ri == len(rows) - 1
        for c in range(ncols):
            val = row[c] if c < len(row) else ""
            cell = gtbl.cell(r0 + ri, c)
            _fmt_cell(cell, str(val), size, bold=is_total,
                      fill=GRAY_HEADER if is_total else WHITE)
    # ruled grid (see _set_cell_borders): on by default for the cost and
    # timeline tables, per-table override via "borders": true/false
    if table.get("borders", borders):
        bw = table.get("border_w", 0.75)
        for r in range(nrows):
            for c in range(ncols):
                _set_cell_borders(gtbl.cell(r, c), width_pt=bw)
    # tighten row heights
    for r in gtbl.rows:
        r.height = Inches(row_h)
    return gtbl


def _fmt_cell(cell, text, size, bold=False, fill=WHITE):
    cell.fill.solid(); cell.fill.fore_color.rgb = fill
    cell.margin_left = Pt(4); cell.margin_right = Pt(4)
    cell.margin_top = Pt(1); cell.margin_bottom = Pt(1)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = cell.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = BLACK


def render_timeline_section(slide, x, y, w, num, title, timeline):
    section_header(slide, x, y, w, f"{num}. {title}")
    box_y = y + HDR_H + GAP
    columns = timeline.get("columns", [])
    row = timeline.get("row", [])
    rows_data = timeline.get("rows")  # allow multiple rows
    table = {"headers": columns,
             "rows": rows_data if rows_data else ([row] if row else []),
             "size": timeline.get("size", 11),
             "row_h": timeline.get("row_h", 0.3)}
    _add_table(slide, x, box_y, w, table, borders=True)


# ===========================================================================
# Five-Whys flowchart
# ===========================================================================
LEGEND_TEXT = {
    "en": [("Legend:  ", "bold"), ("★ bottleneck   ", RED),
           ("◆ unknown-unknown   ", BLUE), ("▲ escalate", BLACK)],
    "ja": [("凡例：  ", "bold"), ("★ ボトルネック　", RED),
           ("◆ 未知の未知　", BLUE), ("▲ 要エスカレーション", BLACK)],
}


def render_five_whys(slide, x, y, w, h, num, title, fw, lang="en"):
    """Header bar + a bordered area containing one horizontal cause-chain per
    'tree'. Each tree: bold problem node at left, then steps flowing right with
    red Why-N labels (centered above each node) and blue curved-down connector
    arrows placed in the gaps between nodes (never overlapping the text). A
    language-aware legend explains the markers."""
    section_header(slide, x, y, w, f"{num}. {title}")
    box_y = y + HDR_H + GAP
    box = content_box(slide, x, box_y, w, h)
    box.text_frame.clear()

    trees = fw.get("trees", [])
    legend = fw.get("legend", True)

    # Inner drawing area — the full width is used for the chains (no side notes).
    pad = 0.12
    area_x = x + pad
    area_y = box_y + pad
    area_w = w - 2 * pad
    area_h = h - 2 * pad - (0.26 if legend else 0)

    n = max(1, len(trees))
    band_h = area_h / n
    for ti, tree in enumerate(trees):
        band_y = area_y + ti * band_h
        _draw_tree(slide, area_x, band_y, area_w, band_h, tree)

    if legend:
        ly = box_y + h - 0.28
        lb = textbox(slide, x + pad, ly, w - 2 * pad, 0.24,
                     anchor=MSO_ANCHOR.MIDDLE)
        p = lb.text_frame.paragraphs[0]
        _para_compact(p)
        for txt, style in LEGEND_TEXT.get(lang, LEGEND_TEXT["en"]):
            if style == "bold":
                _add_run(p, txt, 9, bold=True)
            else:
                _add_run(p, txt, 9, color=style)
    return box


def _draw_tree(slide, x, y, w, h, tree):
    """Lay a single cause chain horizontally across (x,y,w,h): a bold problem
    node at the left, then one node per Why-step. Nodes are narrower than their
    slot so the blue curved arrow sits in the gap between nodes; the red Why-N
    label sits in its own row above each node; node text auto-fits its box."""
    problem = tree.get("problem", "")
    steps = tree.get("steps", [])
    nslots = len(steps) + 1                     # +1 for the problem node
    slot_w = w / max(1, nslots)
    gap = min(0.30, slot_w * 0.30)              # horizontal room for the arrow
    node_w = max(0.4, slot_w - gap)

    label_h = 0.20
    node_y = y + label_h + 0.06
    node_h = max(0.4, h - label_h - 0.14)
    nsize = FLOW_PT  # fixed flowchart font; shorten node text if it overflows

    # Problem node (bold, far left)
    pb = textbox(slide, x, node_y, node_w, node_h, anchor=MSO_ANCHOR.MIDDLE)
    pp = pb.text_frame.paragraphs[0]; pp.alignment = PP_ALIGN.LEFT
    _para_compact(pp)
    _add_run(pp, problem, nsize, bold=True)

    for i, step in enumerate(steps):
        slot_x = x + (i + 1) * slot_w
        # Blue curved arrow in the gap to the LEFT of this node, centered on the
        # node row — clear of both the Why label (above) and the node text.
        aw, ah = 0.24, 0.16
        ax = slot_x - gap / 2 - aw / 2
        ay = node_y + node_h / 2 - ah / 2
        curved_down_arrow(slide, ax, ay, aw, ah)
        # Red Why-N label sits directly ABOVE the arrow it describes.
        why_label(slide, ax + aw / 2, node_y - label_h - 0.02, f"Why-{i+1}")

        if isinstance(step, dict):
            txt = step.get("text", "")
            mark = step.get("mark")
            dashed = step.get("dashed", False)
        else:
            txt, mark, dashed = str(step), None, False
        prefix = {"star": "★ ", "diamond": "◆ ",
                  "triangle": "▲ "}.get(mark, "")
        if dashed:
            sb = content_box(slide, slot_x, node_y, node_w, node_h)
            _dash_border(sb)
            tf = sb.text_frame
        else:
            sb = textbox(slide, slot_x, node_y, node_w, node_h,
                         anchor=MSO_ANCHOR.MIDDLE)
            tf = sb.text_frame
        tf.margin_left = Pt(2); tf.margin_right = Pt(2)
        tf.margin_top = Pt(1); tf.margin_bottom = Pt(1)
        sp = tf.paragraphs[0]; sp.alignment = PP_ALIGN.LEFT
        _para_compact(sp)
        col = RED if mark == "star" else (BLUE if mark == "diamond" else None)
        _add_run(sp, prefix + txt, nsize, color=col)


def _dash_border(shape):
    """Make a shape's outline a blue dashed line (bottleneck/unknown boxes)."""
    _set_line(shape, BLUE, 1.0)
    ln = shape.line._get_or_add_ln()
    d = ln.find(qn('a:prstDash'))
    if d is None:
        d = ln.makeelement(qn('a:prstDash'), {})
        ln.append(d)
    d.set('val', 'dash')


# ===========================================================================
# Header row (top of slide)
# ===========================================================================
def render_header(slide, meta):
    title = meta.get("title", "A3 Report")
    prefix = meta.get("title_prefix")  # e.g. "Example:" shown in red
    left = meta.get("header_left", [])
    right = meta.get("header_right", [])

    # left identity block
    if left:
        lb = textbox(slide, 0.10, 0.05, 4.5, 0.7)
        fill_list(lb.text_frame, left, style="none", size=HEADER_PT)
    # right identity block
    if right:
        rb = textbox(slide, 11.0, 0.05, 2.9, 0.7)
        fill_list(rb.text_frame, right, style="none", size=HEADER_PT)
    # center title in a bordered box
    tb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.2), Inches(0.10),
                                Inches(6.7), Inches(0.50))
    _set_fill(tb, WHITE); _set_line(tb, BLACK, 1.25)
    tb.shadow.inherit = False
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    if prefix:
        _add_run(p, prefix + " ", TITLE_PT, bold=False, color=RED)
    _add_run(p, title, TITLE_PT, bold=False, color=BLACK)


# ===========================================================================
# Main build
# ===========================================================================
# Default right-column vertical grid (top of each section bar), inches.
# Heights are content-box heights (excludes the header bar).
def build(spec, out_path):
    prs = Presentation()
    prs.slide_width = Inches(PAGE_W)
    prs.slide_height = Inches(PAGE_H)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    meta = spec.get("meta", {})
    lang = "ja" if str(meta.get("language", "en")).lower().startswith("ja") \
        else "en"
    render_header(slide, meta)

    # ---- LEFT COLUMN -----------------------------------------------------
    # 1 Background, 2 Current Problems, 3 Goals, 4 Five-Whys
    render_simple_section(slide, LCOL_X, 0.76, COL_W, 1.64, 1,
                          spec.get("titles", {}).get("background", "Background"),
                          spec.get("background", []))
    render_simple_section(slide, LCOL_X, 2.78, COL_W, 1.51, 2,
                          spec.get("titles", {}).get("current_problems",
                                                     "Current Problems"),
                          spec.get("current_problems", []))
    render_simple_section(slide, LCOL_X, 4.71, COL_W, 0.71, 3,
                          spec.get("titles", {}).get("goals", "Goals"),
                          spec.get("goals", []))
    fw = spec.get("five_whys", {})
    render_five_whys(slide, LCOL_X, 5.81, COL_W, 4.14, 4,
                     spec.get("titles", {}).get("five_whys",
                                                "Five-Whys Analysis"),
                     fw, lang=lang)

    # ---- RIGHT COLUMN ----------------------------------------------------
    # 5 Deep/Ergonomic Analysis, 6 Countermeasures/Solutions, 7 Cost, 8 Timeline
    da = spec.get("deep_analysis", {})
    render_simple_section(slide, RCOL_X, 0.76, COL_W, 2.63, 5,
                          da.get("title",
                                 spec.get("titles", {}).get("deep_analysis",
                                                            "Deep Analysis")),
                          {"blocks": da.get("blocks")} if da.get("blocks")
                          else da.get("items", []))
    cm = spec.get("countermeasures", {})
    render_simple_section(slide, RCOL_X, 3.77, COL_W, 2.59, 6,
                          cm.get("title",
                                 spec.get("titles", {}).get("countermeasures",
                                                            "Countermeasures")),
                          {"blocks": cm.get("blocks")} if cm.get("blocks")
                          else cm.get("items", []))
    cost = spec.get("cost_analysis", {})
    render_cost_section(slide, RCOL_X, 6.78, COL_W, 7,
                        spec.get("titles", {}).get("cost_analysis",
                                                   "Cost Analysis"),
                        cost, bottom_limit=9.24)
    tl = spec.get("timeline", {})
    render_timeline_section(slide, RCOL_X, 9.24, COL_W, 8,
                            spec.get("titles", {}).get("timeline", "Timeline"),
                            tl)

    prs.save(out_path)

    # validate by reloading
    Presentation(out_path)
    return out_path


def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: python build_a3.py spec.json output.pptx\n")
        sys.exit(1)
    spec_path, out_path = sys.argv[1], sys.argv[2]
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    build(spec, out_path)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
