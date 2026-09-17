---
name: a3-report
description: >
  Create a one-page A3 problem-solving report as a PowerPoint (.pptx) that
  exactly matches the classic A3/IE format: 14x10.5" landscape, two columns,
  numbered black section-header bars (1. Background ... 8. Timeline), a visual
  Five-Whys flowchart, a cost table, and a timeline table. Use whenever the user
  asks for an "A3 report", "A3 sheet", "A3改善シート", "A3 problem-solving
  sheet", "Five Whys" / "5 Whys" report, root-cause analysis sheet,
  kaizen / カイゼン / 改善 report, improvement plan, or a "problem-solving
  PowerPoint" — or describes wanting a single-page, structured
  problem → root-cause → countermeasure → plan deck even without saying "A3".
  Also trigger when the user points to an existing A3 example/template and wants
  one made "in the same format", or asks to draw a Five-Whys / cause-chain
  flowchart for a problem.
---

# A3 Report Creation

Create a human-centered, one-page A3 problem-solving report (PowerPoint) that
reproduces the reference format precisely. An A3 is not a document-formatting
exercise — it is **guided thinking** compressed onto one page. Your job is to
help the user discover what is really happening, why, which cause is the real
bottleneck, and what to do first; the PowerPoint is only the final artifact.

The format, fonts, colors, arrows, and tables are owned by the bundled builder
script `scripts/build_a3.py`, so the output never drifts from the reference. Your
job is to produce excellent *content* in a JSON spec and hand it to the script.
The cost table (7) and timeline (8) are ruled with a black grid by default —
see `"borders"` in `references/spec_schema.md` if a table needs it turned off.

## The format (what every A3 looks like)

A3 landscape, two columns, with eight numbered sections in black header bars:

```
┌─ header: org/course (left) │ [Title box] │ section/ID (right) ─┐
│ 1. Background              │ 5. Deep / Ergonomic Analysis      │
│ 2. Current Problems        │ 6. Countermeasures / Solutions    │
│ 3. Goals                   │ 7. Cost Analysis (bullets+table)  │
│ 4. Five-Whys Analysis      │ 8. Timeline (month/day table)     │
│    (flowchart)             │                                   │
└────────────────────────────┴───────────────────────────────────┘
```

See `assets/reference_example.pptx` for the canonical look and
`assets/example_spec.json` for a complete, working spec that reproduces it.
When in doubt about layout, open the reference.

## Workflow

### 1. Understand depth, then dialogue accordingly

A good A3 comes from real thinking, so gather genuine substance before
generating. **Scale your questioning to how much the user already gave you:**

- If the user dumps a rich description (a real situation, specific problems,
  numbers, a deadline), confirm the key sections and fill gaps — don't
  interrogate them for the sake of a quota.
- If the user is vague ("make me an A3 about my messy workflow"), use the spiral
  dialogue: ask a small group of questions, listen, draft a section, confirm
  ("これでいいですか? / Is this right?"), then continue. The Five-Whys is where
  depth matters most — keep asking "why" down each cause chain until you reach
  something actionable, not just a restatement.
- If the user explicitly says "just generate it" or gives you a finished
  write-up, generate directly and ask only about true blockers.

Match the user's language. If they write in Japanese, produce the report in
Japanese and confirm in Japanese; if English, use English. The section labels,
bullets, flowchart text, and tables all follow the user's language.

**First question, every time: "これは前回の課題解決の続きですか？ / Is this
a continuation of a previous A3?"** If yes, switch to the iteration workflow
(see "Iterating" below) and interview the previous countermeasures one by one
before anything else: 「これはやった？どうだった？なぜうまくいった？なぜ
失敗した？何か新しい気づきは？」— did you do it, what happened, why did it
work, why did it fail, any new insight. Results, not intentions, drive the
No.2 sheet.

**Always ask when the next review will be** ("次のレビュー（次のA3）は
3日後？来週？1か月後？1年後？"). The Timeline must be sized to end at that
review date, with the review itself as the final milestone — an A3 whose
timeline doesn't land on the next Check has no closing date for its PDCA
loop. The cycle length should also match the goal's measurement window: a
"1か月でけんか0件" KPI cannot be judged by a 1-week cycle. Record the agreed
date; the No.2 sheet starts from it.

The eight sections to cover (see `references/a3_format.md` for what each one
captures and the Deep-Analysis knowledge patterns):

1. Background / Current Situation
2. Current Problems
3. Goals
4. Five-Whys Analysis  ← the core; must be visual
5. Deep Analysis (rename to fit the domain, e.g. "Ergonomic Analysis")
6. Countermeasures (rename to fit, e.g. "Proposed Solutions")
7. Cost Analysis (money **and** time **and** attention)
8. Timeline (concrete deliverables per period)

#### Escalation is part of the analysis (▲) — not everything is self-solvable

A Five-Whys that ends only in "things I will fix myself" is usually dishonest.
For **every root cause**, apply the five escalation tests in
`references/a3_format.md` (§2b): does fixing it require **authority**,
**resources**, **expertise**, **scope**, or **deadline speed** that the user
does not have? If any test hits, that root cause is an escalation item — mark
it `"mark": "triangle"` (▲) and treat "ask X for Y by Z" as the countermeasure.

**Requirement: at least 1, ideally 2, of the root causes across the trees must
be ▲ escalation items** (help from a boss, senior colleague, vendor, external
expert, government program, or community). If the analysis truly produced
none, ask the user directly: "この中で、あなた一人の権限・資源・専門性で本当に
解決できないものはどれですか？" before finalizing.

#### Deep Analysis must surface what the user can't see

This is the section that earns the A3 its keep. The user already knows their own
situation; what they're paying you for is **expert insight they would not reach
on their own.** So the Deep Analysis should explicitly include:

- **Hidden strengths** — assets the user is undervaluing or hasn't connected to
  the problem (e.g., a niche skill that is suddenly in demand, breadth that reads
  as proof of transferable ability rather than lack of focus).
- **Hidden risks / blind spots** — failure modes, market realities, or
  second-order effects the user is not accounting for.
- **Escalation / external help (エスカレーション先)** — for each ▲ root cause,
  **use web search to find what a boss or external party can concretely
  provide**, and write it in: subsidy/support programs, vendor services,
  standard tools, consultants, communities, or the specific leverage a manager
  has (budget approval, cross-department pull, introductions). Name the source
  and what to ask for — "上司に◯◯の決裁を依頼", "◯◯補助金 (経産省, 2026) が
  該当", not "誰かに相談する".

**Do real web research before writing it.** Use web search to ground these in
the current world — emerging-field demand, salary/market signals, whether a job
category even exists, recent reports, regulatory shifts. Bring back specific,
sourced "うんちく" (e.g., "X is the top finding of the 2026 AI Safety Report",
"there is no hiring category called Y in Japan, so map to Z"), not generic
platitudes. Concrete, surprising, verifiable insight is the goal. Search a few
targeted queries, then distill the 2-4 findings that most change the user's
plan. This research-backed expert layer is what separates a useful A3 from a
pretty form.

**Apply the Human Factors / resilience lens** in
`references/human_factors_lens.md` — a 30-point checklist (local rationality,
context constraints, automation traps, org/communication gaps, resilience) in
the Dekker/Hollnagel/Woods tradition. Use it for **both** core sections:

- **Five-Whys:** frame every cause as a property of the *system / situation* via
  the actor's local rationality — never "carelessness" or "lack of awareness".
  An error is the start of the analysis (a symptom), not the conclusion.
- **Deep Analysis → Unknown Unknowns (◆):** write the user's blind spots as the
  intersection of your **web findings** and whichever of the 30 lenses *hit*
  (e.g. an opaque auto-screening pipeline = "silent scaffolding / opacity"; a
  user judging their own past choices as failures = hindsight bias vs local
  rationality; "doing the activity = safe" = the too-narrow definition of safe).
  Tag each with its lens so the insight is traceable; surface the 2-4 that most
  change the plan rather than forcing all 30.

### 2. Build the JSON spec

Assemble the content into a JSON spec. The full schema, every field, and the
Five-Whys flowchart structure are in `references/spec_schema.md` — **read it
before writing the spec.** Start from `assets/example_spec_jobhunt_ja.json`
(the current best-practice model: ★/◆/▲ marks, blocks, tight text) and adapt
it. `assets/example_spec.json` reproduces the classic reference layout but
predates the escalation/verification rules — use it for layout questions only.

Key content principles, baked into the format for a reason:

- **Fixed type sizes — fit by editing, not shrinking.** All body text is a
  uniform **13 pt**, section header bars **16 pt**, and everything in the
  Five-Whys flowchart **12 pt**. The script does **not** auto-shrink to fit: if a
  section's content is too long it will overflow, and the builder prints a
  `[overflow] section '...'` warning on stderr. When you see that warning, the
  fix is to **rewrite the content shorter** (fewer words, fewer/merged bullets),
  not to change the font. Uniform sizing looks deliberate and avoids the "tiny
  text in a half-empty box" problem. Write short bullets, action word first.
- **Keep dense sections lean so they fit at 13 pt.** Goals (~3 lines), Cost
  bullets (~4 one-line bullets + a ≤6-row table), and Sections 5 & 6 are the
  tightest. For 5 & 6 use `blocks` (bold heading + colored sub-points) and keep
  each point to roughly one line. Rebuild and check stderr for overflow.
- **Mark the thinking, not just the facts.** In the Five-Whys, flag the real
  bottleneck with `"mark": "star"` (★), unknown-unknowns with `"diamond"` (◆),
  and escalation with `"triangle"` (▲). Put bottleneck/unknown nodes in dashed
  boxes (`"dashed": true`). This is what turns a cause list into analysis.
  **An A3 with no ★ hasn't finished its analysis; an A3 with no ▲ hasn't been
  honest about its limits** (≥1 ▲ required, 2 recommended — see the escalation
  tests above).
- **Traceability: every marked root cause gets a countermeasure.** Each ★/▲/◆
  must map to at least one item in section 6 — no orphaned root causes, no
  countermeasures that fix nothing. For every ▲, the countermeasure must name
  **who to ask, what to ask for, and by when** (誰に・何を・いつまでに).
- **Close the PDCA loop.** Goals must contain numbers (KPI, %, deadline), and
  the Timeline must include at least one **verification milestone** where that
  KPI is actually measured (効果測定/検証/review) — not only "do" tasks.

### 3. Generate and verify

**First lint the spec** — the content-quality rules (★ present, ≥1 ▲
escalation, chain depth, traceability keywords, numeric goals, a verification
milestone, cost-table size) are enforced mechanically, so nothing depends on
memory:

```bash
python scripts/validate_spec.py spec.json
```

Fix every `[WARN]` by editing the spec (exit code 1 means warnings remain),
then run the builder:

```bash
python scripts/build_a3.py spec.json output.pptx
```

The script validates the file by reloading it. Then **render it to an image and
look at it** before showing the user — this catches overflow and layout issues
the JSON can't reveal. If LibreOffice is available:

```bash
soffice --headless --convert-to pdf output.pptx   # then view the PDF
```

On Windows with PowerPoint installed, export a slide PNG via COM (PowerShell):

```powershell
$p = New-Object -ComObject PowerPoint.Application
$d = $p.Presentations.Open("output.pptx",$true,$false,$false)
$d.Slides.Item(1).Export("preview.png","PNG",1500,1125); $d.Close(); $p.Quit()
```

Check: every section populated and readable, no text clipped (especially the
cost bullets/table and the long sections 5–6), the flowchart arrows and Why-N
labels line up, and font sizes look ≥10 pt. If a section overflows, shorten its
content rather than fighting the layout.

### 4. Deliver and iterate

Give the user the `.pptx` path plus a preview image. Then ask whether to refine
the Deep Analysis, Five-Whys, wording, or fit — and loop. The first draft is a
starting point for the user's thinking, not the end.

## Iterating: No.2 and beyond (the real kaizen loop)

One A3 is a plan; kaizen is the loop. When the user returns for the next cycle
(or an existing sheet's title says No.N / 第N回), build the next sheet with
these rules — see `references/a3_format.md` §6 for the full pattern:

1. **Open with the Check.** Interview the user on every previous
   countermeasure, then put a results table in **section 2** (`"table"` in
   `current_problems` — the builder renders it under the items). Judge each
   row twice: 実施 (did it happen) and 効果 (did it move the KPI), with
   ◎ effective / ○ done, effect still under observation / △ partial /
   × not done / － not judgeable. **実施≠効果** — "we did it" is not
   "it worked".
2. **No silent drops.** Any previous item now 未実施/保留/中止 — especially a
   ▲ — must get a written reason plus a **re-trigger condition** ("口論が
   月2回 or 過熱1回 → 48時間以内に予約"). One calm month is not proof the
   system is fixed; "good results = safe to skip" is the narrow definition
   of safety.
3. **Update the Five-Whys as tested hypotheses.** Causes the results confirmed
   stay; refuted causes are replaced; new causes revealed by the cycle's data
   (e.g. the one fight that still happened) get their own tree. The ★ usually
   moves — the old bottleneck was treated, so find the next one.
4. **Graduate what worked (SDCA / 歯止め).** Effective measures leave the
   countermeasures list: standardize/automate them (reminders, routines) and
   note them as 定着済み in the background or deep analysis. Section 6 is for
   the *next* moves, not a museum of past ones.
5. **Number and link the cycles.** Title carries "（No.N）", the header date
   is the review date, and the background recaps the previous cycle in one
   line. Ask the next review date again and end the new timeline on it
   (final milestone = "No.N+1 レビュー").
6. Lint as usual — `validate_spec.py` checks iteration sheets for the Check
   table, per-row 判定 marks, and re-trigger conditions on dropped items.

## Notes

- The builder needs `python-pptx` (`pip install python-pptx`).
- Every section is optional in the spec — a missing section leaves its grid slot
  empty — but a complete A3 has all eight. Don't ship a half-empty sheet unless
  the user asked for a partial draft.
- To embed a photo (e.g. in Current Problems), set `"image"` to a file path in
  that section's spec object.
