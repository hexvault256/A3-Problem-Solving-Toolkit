# A3 Problem-Solving Toolkit

A practical toolkit for creating **one-page A3 problem-solving reports in PowerPoint** using structured JSON, Five-Whys analysis, Human Factors thinking, and a repeatable validation workflow.

The goal is not only to make a good-looking A3 sheet. The toolkit is designed to support **guided problem solving**: understand the situation, identify root causes, surface hidden risks, choose countermeasures, and close the PDCA loop with measurable follow-up.

## What this toolkit does

It generates a one-page `.pptx` A3 report with a consistent classic IE/A3 layout:

- Background / Current Situation
- Current Problems
- Goals
- Five-Whys Analysis
- Deep Analysis
- Countermeasures / Solutions
- Cost Analysis
- Timeline

The PowerPoint layout is generated automatically so the author can focus on the **quality of the analysis and content**, rather than manually drawing boxes, arrows, and tables. The builder controls the format, fonts, colors, arrows, tables, and overall page geometry. fileciteturn1file1L103-L115

## Key ideas

### 1. Five-Whys with traceability

The Five-Whys section is not intended to be a simple list of causes. The toolkit can mark:

- **★ Bottleneck** — the root cause that most strongly constrains the result
- **◆ Unknown Unknown** — an important blind spot or unvalidated assumption
- **▲ Escalation** — a cause that cannot realistically be solved by the user alone

Every marked cause should connect to a concrete countermeasure. For an escalation item, the action should specify **who to ask, what to ask for, and by when**. fileciteturn1file3L224-L237

### 2. Human Factors / systems thinking

The toolkit includes a 30-point Human Factors / resilience lens covering:

- hindsight bias and blame
- local rationality
- situational constraints
- automation and tool mismatch
- organizational / communication gaps
- resilience and adaptive capacity

The basic principle is: **do not stop at “human error.”** Treat error as the start of the analysis and look for the system conditions that made the action reasonable at the time. fileciteturn0file3L23-L30

### 3. Deep Analysis

The Deep Analysis section is designed to go beyond what the user already knows. It can surface:

- hidden strengths
- hidden risks and blind spots
- external support or escalation options
- expert/domain knowledge
- relevant Human Factors insights

The intent is to identify a few insights that materially change the plan, rather than filling the page with generic advice. fileciteturn1file5L368-L395

### 4. PDCA / Kaizen loop

A3 is treated as an iterative process rather than a one-time document.

Goals should contain measurable KPIs or deadlines, and the timeline should include a verification point where the result is actually checked. Later A3 cycles can review which countermeasures were implemented and whether they actually worked. fileciteturn1file0L10-L16

---

## Repository contents

| File | Purpose |
|---|---|
| `SKILL.md` | Main instructions and workflow for creating an A3 report |
| `build_a3.py` | Generates the one-page PowerPoint from a JSON specification |
| `validate_spec.py` | Checks the JSON specification before generation |
| `spec_schema.md` | Reference for the JSON schema |
| `a3_format.md` | Guidance for the eight A3 sections and problem-solving logic |
| `human_factors_lens.md` | 30-point Human Factors / resilience analysis lens |
| `example_spec.json` | Classic example specification |
| `example_spec_jobhunt_ja.json` | Japanese example using the extended analytical approach |
| `reference_example.pptx` | Reference A3 PowerPoint showing the intended layout |

The JSON schema supports the eight main A3 sections: background, current problems, goals, Five-Whys, deep analysis, countermeasures, cost analysis, and timeline. fileciteturn0file5L7-L20

---

## Requirements

- Python 3
- [`python-pptx`](https://python-pptx.readthedocs.io/)

Install the PowerPoint library:

```bash
pip install python-pptx
```

`validate_spec.py` uses only the Python standard library. fileciteturn1file4L275-L287

---

## Quick start

### 1. Start from an example JSON file

Copy one of the example specifications and edit the content:

```bash
cp example_spec.json my_problem.json
```

For a more advanced example with ★ / ◆ / ▲ analytical markers, use:

```bash
cp example_spec_jobhunt_ja.json my_problem.json
```

### 2. Validate the specification

```bash
python validate_spec.py my_problem.json
```

The validator checks content-quality rules such as:

- Five-Whys depth
- presence of a ★ bottleneck
- escalation items
- measurable goals
- traceability
- verification milestones
- table/content constraints

Exit codes:

- `0` — OK
- `1` — warnings found
- `2` — unreadable or invalid JSON

fileciteturn1file4L275-L287

### 3. Generate the PowerPoint

```bash
python build_a3.py my_problem.json output.pptx
```

The builder creates a **14 × 10.5 inch landscape PowerPoint** with the A3 layout, Five-Whys flowchart, tables, and timeline. fileciteturn0file6L3-L14

### 4. Review the output visually

Always open the generated PowerPoint and check:

- no clipped text
- readable font sizes
- Five-Whys arrows and labels are aligned
- cost and timeline tables fit
- sections 5 and 6 are concise enough

If a section becomes too dense, shorten the content instead of shrinking it into unreadable text. fileciteturn1file3L257-L264

---

## Example workflow

```text
Problem description
       ↓
Structured discussion / analysis
       ↓
JSON specification
       ↓
validate_spec.py
       ↓
Fix warnings
       ↓
build_a3.py
       ↓
PowerPoint A3
       ↓
Review results / KPI
       ↓
Next A3 cycle
```

---

## A3 structure

```text
┌─────────────────────────────────────────────────────────────┐
│ Organization / Context        Title           Owner / Date  │
├──────────────────────────────┬──────────────────────────────┤
│ 1. Background                │ 5. Deep Analysis             │
│ 2. Current Problems          │ 6. Countermeasures           │
│ 3. Goals                     │ 7. Cost Analysis             │
│ 4. Five-Whys Analysis        │ 8. Timeline                  │
│    → visual cause chain      │                              │
└──────────────────────────────┴──────────────────────────────┘
```

The format is intentionally consistent so that attention stays on the **reasoning**, not on redesigning the slide every time. fileciteturn1file1L117-L133

---

## Example use cases

This toolkit can be adapted to problems such as:

- manufacturing quality problems
- productivity and process improvement
- Human Factors / ergonomic problems
- safety and human-error analysis
- project-management problems
- service-process improvement
- job-search strategy
- organizational problems
- personal workflow improvement

The included classic example analyzes ergonomic problems in a study room and connects problems such as a messy desk and neck pain to Five-Whys analysis, ergonomic analysis, proposed solutions, cost analysis, and a timeline. fileciteturn0file1L26-L40 fileciteturn0file1L55-L87

---

## Design philosophy

### Fix the system, not only the person

A major principle of this toolkit is to avoid stopping at explanations such as:

> “The person was careless.”

Instead ask:

> “Why did this action make sense to the person in that situation?”

Then investigate constraints, information, tools, incentives, workload, communication, organizational boundaries, and safeguards. fileciteturn0file3L23-L40

### Make goals measurable

A goal should contain a KPI, count, percentage, deadline, or another observable success condition.

### Separate action from effect

“Implemented” does not automatically mean “effective.” Later A3 cycles should check both whether an action was carried out and whether it improved the target KPI. fileciteturn1file6L434-L465

### Keep the report readable

The A3 sheet is deliberately constrained to one page. If the content does not fit, simplify the wording and prioritize the most important information.

---

## Files to read first

If you are exploring the toolkit for the first time, a useful order is:

1. `reference_example.pptx`
2. `example_spec.json`
3. `SKILL.md`
4. `a3_format.md`
5. `human_factors_lens.md`
6. `spec_schema.md`
7. `validate_spec.py`
8. `build_a3.py`

---

## Author

**Takeaki Toma, Ph.D.**  
Industrial Engineering / Human Factors / Quality / Statistics / AI

This project combines classic Industrial Engineering problem-solving with Human Factors, systems thinking, structured validation, and AI-assisted analysis.
