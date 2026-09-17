# A3 Spec Schema

The builder `scripts/build_a3.py` takes one JSON object. Every key is optional;
omitted sections leave their grid slot blank. A complete A3 uses all of them.
Start from `assets/example_spec.json` (a known-good spec) and adapt it.

## Top-level shape

```json
{
  "meta": { ... },
  "titles": { ... },          // optional per-section title overrides
  "background": [ ... ],       // section 1
  "current_problems": { ... }, // section 2
  "goals": [ ... ],            // section 3
  "five_whys": { ... },        // section 4  (the flowchart)
  "deep_analysis": { ... },    // section 5
  "countermeasures": { ... },  // section 6
  "cost_analysis": { ... },    // section 7
  "timeline": { ... }          // section 8
}
```

## meta (header row)

```json
"meta": {
  "title": "Improving Ergonomic Problems in my room",
  "title_prefix": "Example:",          // optional; shown in red before title
  "header_left":  ["Org / team line 1", "Course / context line 2"],
  "header_right": ["Section / dept", "ID, Name"],
  "language": "en"                      // free-form note; report follows it
}
```

## titles (optional overrides)

Section 5 defaults to "Deep Analysis" and section 6 to "Countermeasures".
Rename them to fit the domain (the reference uses "Ergonomic Analysis" and
"Proposed Solutions"). You can override any of:

```json
"titles": {
  "background": "Background", "current_problems": "Current Problems",
  "goals": "Goals", "five_whys": "Five-Whys Analysis",
  "deep_analysis": "Ergonomic Analysis", "countermeasures": "Proposed Solutions",
  "cost_analysis": "Cost Analysis", "timeline": "Timeline"
}
```
(`deep_analysis` and `countermeasures` also accept a `"title"` inside their own
object, which takes precedence.)

## Simple list sections (1, 3)

A plain array of strings → a bulleted list:

```json
"background": [
  "AUM started online classes from March...",
  "Sitting 12+ hours makes me exhausted...",
  "I want to resolve my study-room problems."
]
```

A list item may instead be an object for per-item color/bold:
`{"text": "...", "color": "red", "bold": true}`.

## current_problems (section 2)

Supports a marker style, an optional photo, and an optional **table** (used
by iteration sheets No.2+ for the previous-round results / Check table — it
renders below the items, inside the section box):

```json
"current_problems": {
  "style": "roman",          // bullet | roman | number | alpha-lower | alpha-upper | none
  "items": ["My desk is messy.", "I sit with bad posture.", "..."],
  "image": "/abs/path/photo.jpg",   // optional; placed top-right inside the box
  "image_w": 2.15, "image_h": 1.45, // optional inches
  "table": {                         // optional; iteration Check table
    "headers": ["前回の施策", "実施", "効果"],
    "rows": [["チェックイン15分/週", "○ 4/4回", "◎ 不満7/9件改善"]],
    "size": 9,                       // keep rows ≤7 or the section overflows
    "borders": true                  // optional; unruled here unless set
  }
}
```

When a table is present the item list gets the remaining height — keep items
to 1-2 lines (e.g. a single 判定 legend line) and rows to ≤7. Unlike the cost
and timeline tables, this one is **unruled by default** (it sits inside a
bordered content box); add `"borders": true` to rule it as well.

## deep_analysis (5) and countermeasures (6) — `blocks`

These two sections hold the most text and use **blocks**: a bold heading
followed by an indented, marker-prefixed, colored sub-point list. This matches
the reference (black bold headings, red questions in §5; blue lettered solutions
in §6).

```json
"deep_analysis": {
  "title": "Ergonomic Analysis",
  "blocks": [
    {
      "heading": "A. Used Ergonomics checklist for item-lost problems",
      "point_color": "red",        // applies to all points in this block
      "style": "bullet",           // marker for the points
      "points": [
        "Perhaps labels or color could be utilized?",
        "Will a better workstation layout eliminate searching?"
      ]
    }
  ]
}
```

```json
"countermeasures": {
  "title": "Proposed Solutions",
  "blocks": [
    {"heading": "Solutions for the messy/search problems",
     "style": "alpha-lower", "point_color": "blue",
     "points": ["Change the workstation layout", "Buy containers and a bookshelf"]},
    {"heading": "Solutions for the posture/neck-pain problems",
     "style": "alpha-upper", "point_color": "blue",
     "points": ["Adjust chair, then keyboard/mouse, then monitor", "..."]}
  ]
}
```

`heading_color` (default black) and per-point `{"text","color"}` are also
available. If you don't need headings, you can instead pass `"items": [...]`
(a plain list) to either section.

Color names accepted anywhere: `red, blue, black, white, green`, or a hex string
like `"2E5BA8"`.

## cost_analysis (section 7)

Bullets + an optional table. This is the **tightest** slot vertically; keep it to
~4 short bullets and ≤6 data rows so nothing is clipped. The script auto-fits the
table above the Timeline and shrinks the table font as needed.

A bullet can be a plain string, or an object `{"label": "...", "text": "..."}`
where `label` is rendered **bold** before the text (with a `：`). Use this for the
money / time / attention / constraint headings so they stand out:

```json
"cost_analysis": {
  "bullets": [
    {"label": "Money", "text": "≈¥0 — videos self-made, free tools."},
    {"label": "Time",  "text": "30–60 min per tailored application."},
    {"label": "Attention", "text": "Stop scattering; focus on the critical path."},
    "Plain strings without a bold label also work."
  ],
  "table": {
    "headers": ["Items", "Price(KD)", "Years", "Hours", "KD/Hour"],
    "rows": [
      ["Light stand", "10", "30", "1260000", "0.0000079"],
      ["Total", "418", "", "Total", "0.0022365"]
    ],
    "highlight_last": true,  // gray-fills the final (Total) row
    "borders": true,         // default true here — ruled grid on every cell
    "border_w": 0.75         // optional line width in pt (default 0.75)
  }
}
```

The cost table is **ruled by default**: every cell gets a 0.75pt black grid.
A PowerPoint table otherwise inherits a theme style whose lines are white, so
white-filled cells render with no visible grid at all. Set `"borders": false`
to go back to the unruled look.

## timeline (section 8)

A month/period table. One header row + one assignment row (or several with
`rows`):

```json
"timeline": {
  "columns": ["July", "August", "September", "October", "November", "December"],
  "row": ["a, c, d, A, B,D", "b, F", "", "C", "", "E"]
}
```
For a day-by-day plan use `"columns": ["Day 1","Day 2", ...]`. Multiple rows:
`"rows": [["..."],["..."]]` (e.g. a "Deliverable" row under a "Task" row).

The timeline is **ruled by default** (0.75pt black grid on every cell), same as
the cost table. `"borders": false` turns it off; `"border_w"` sets the pt width.

## five_whys (section 4) — the flowchart

The core. One **tree** per problem; each tree is a horizontal cause chain that
flows left→right with a bold problem node at the far left, red "Why-1…Why-N"
labels above blue curved connector arrows, and the cause text in each slot.

```json
"five_whys": {
  "trees": [
    {
      "problem": "Items lost",
      "steps": [
        "Because it takes time to find",
        "Desk is messy",
        "Everything on desk",
        {"text": "No home-position for items", "mark": "star", "dashed": true},
        {"text": "No containers for small items", "dashed": true}
      ]
    },
    {
      "problem": "Neck pain",
      "steps": [
        "Bend my back (kyphosis)",
        "Because I want to see the PC screen",
        "Text size is small",
        {"text": "Did not change PC settings", "mark": "star", "dashed": true}
      ]
    }
  ],
  "notes": [
    "We can evaluate progress by time-to-find iPhone, keys, wallet.",
    "Evaluate progress by subjective neck-pain feeling."
  ],
  "legend": true
}
```

A **step** is either a plain string or an object:

| Field    | Meaning |
|----------|---------|
| `text`   | the cause text |
| `mark`   | `"star"` ★ bottleneck (red) · `"diamond"` ◆ unknown-unknown (blue) · `"triangle"` ▲ escalate — beyond the user's own authority/resources/expertise/scope/deadline; **≥1 required, 2 recommended** (see `a3_format.md` §2b) |
| `dashed` | `true` draws the node in a dashed blue box (use for bottlenecks/unknowns) |

**Guidance for good flowcharts:**
- Use 2–3 trees (the highest-priority problems). Each tree reads as one row, so
  the whole chart stays scannable. More than 3 trees gets cramped.
- **Aim for a full 5-step chain (Why-1 … Why-5)** where the analysis supports it
  — that's the whole point of "Five Whys". Flowchart text is a **fixed 12 pt**
  (it does not shrink), and a 5-step chain makes each slot narrow, so keep step
  text very short (≈3–6 chars / a couple of words). The last step is usually the
  root cause and a good place for the ★ marker.
- Always mark the real bottleneck with `"mark": "star"` and put it in a dashed
  box. An A3 with no ★ hasn't finished its analysis; an A3 with no ▲ hasn't
  been honest about its limits.
- Every ★/▲/◆ node needs a matching countermeasure in section 6 (for ▲:
  who to ask, what for, by when). Run `python scripts/validate_spec.py
  spec.json` before building — it lints all of these rules automatically.
- `legend` adds the ★/◆/▲ key at the bottom, **automatically in the report's
  language** (Japanese legend for a Japanese A3, English for English) based on
  `meta.language`. Set everything else (problem labels, step text) in the same
  language too.
- The red **Why-N labels sit directly above the blue curved arrows** (which live
  in the gaps between nodes), so neither the labels nor the arrows overlap the
  node text.

### How the layout works (so you can predict the result)

Each tree gets an equal horizontal band inside the section-4 box. Within a band,
the problem node + N steps share the width evenly, so fewer steps = wider, more
readable slots. The blue curved-down arrows sit in the gaps between nodes with
the red Why-N label centered above each arrow. This reproduces the reference's visual
language (problem at left, why-chain flowing right, dashed bottleneck boxes) in a
clean, reproducible way rather than pixel-copying the hand-drawn original.
