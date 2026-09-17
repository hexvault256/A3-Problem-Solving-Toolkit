# A3 Content Guide — what each section captures + thinking patterns

This is the substance behind the eight sections. Use it to ask better questions
and to write content that actually helps the user think, not just fill boxes.

## Table of contents
1. What each section captures
2. The Five-Whys, done well
3. Deep-Analysis knowledge patterns
4. Job-hunt A3 pattern (a worked template)
5. Pre-generation and output checklists

---

## 1. What each section captures

**1. Background / Current Situation** (3–5 bullets) — Who/what/where, the
current context, why this matters *now*, relevant strengths or constraints.

**2. Current Problems** (3–5 bullets) — The main problem, secondary problems,
the risk if nothing changes, and how others perceive the situation. Numbered
(Roman) so later sections can reference "problems I, V".

**3. Goals** — Main goal, deadline, success metric/KPI, minimum acceptable
outcome, stretch outcome. Make them measurable.

**4. Five-Whys Analysis** — The core. See section 2 below.

**5. Deep Analysis** (rename to the domain) — Expert insight that goes beyond the
user's words. Should answer: Why is this the *real* bottleneck? Why will the
countermeasure work? What's the hidden risk? What must the user **stop** doing?
What must they do **first**? Draw on the patterns in section 3.

This section must surface **what the user cannot see themselves** — and it should
be grounded in **web research**, not just reasoning from the conversation:

- **Hidden strengths (気づいていない強み):** assets the user undervalues or hasn't
  linked to the problem. Often a skill that the market has just started to demand,
  or "breadth" that is better framed as *transferable, non-overfit* capability.
- **Hidden risks / blind spots (気づいていないリスク):** market realities, failure
  modes, or second-order effects they're ignoring. A classic one: the user's
  desired title has *no hiring category*, so they must translate it into an
  existing one the screener recognizes.
- **Escalation / external help (エスカレーション先):** for each ▲ root cause,
  **web-search what a boss or an external party can concretely do**, and write
  the findings in. Search patterns: `<問題領域> 補助金 2026`, `<課題> 外部支援
  中小企業`, `<tool category> vendor comparison`, `<課題> コンサル 相場`. Good
  entries name the source and the ask: "IT導入補助金2026の対象 — 上司に申請
  承認を依頼", "ものづくり補助金で設備更新可 (中小企業庁)", "X社の月額SaaSで
  内製不要 (¥3万/月)". Bad entries: "外部に相談する" (who? for what?).

**Research workflow:** run a few targeted web searches (emerging-field demand,
salary/market signals, whether the job/category exists, recent authoritative
reports, regulatory shifts). Distill the 2-4 findings that most change the plan,
and write them as specific, **sourced** "うんちく" — e.g. "automation bias /
over-reliance is a top finding of the International AI Safety Report 2026" or
"there is no 'X specialist' job category in Japan; map to 品質保証 / 安全管理 /
AIガバナンス". Avoid generic advice; concrete and verifiable beats polished and
vague. Cite the gist of the source inline so the user can trust and follow up.

**Apply the 30-point Human Factors / resilience lens in
`human_factors_lens.md`.** Write the Unknown Unknowns (◆) as the intersection of
your web findings and whichever lenses *hit* (local rationality vs hindsight
blame, automation "silent scaffolding"/opacity, double binds, too-narrow
definition of "safe", fragility chains, countermeasures that don't rely on
"human effort"). Use the same lens in the Five-Whys to keep causes system-framed,
not person-blaming. Tag each Unknown Unknown with the lens it came from.

**6. Countermeasures / Solutions** (rename to the domain) — Primary and secondary
countermeasures, the target stakeholder, delivery channel, output artifacts, and
a backup plan. Every countermeasure must be *executable* — a verb the user can
do this week, not an aspiration.

**7. Cost Analysis** — Money cost, **time** cost, **attention** cost, the main
constraint, expected return, and the ROI logic. Do not ignore non-money cost; an
A3 that only counts dollars is incomplete.

**8. Timeline** — Day-by-day for short projects (Day 1–Day 14), weekly for
longer ones. Each period needs a concrete deliverable and a completion
definition, not just "work on X".

---

## 2. The Five-Whys, done well

The point is to walk *down* a cause chain until you hit something you can act on.
A chain that ends in a restatement of the problem ("...because the desk is
messy") isn't finished — keep asking why the desk is messy until you reach a
root like "no home-position for items" or "no daily 5-minute routine".

- Build 2–3 chains for the highest-priority problems (more gets cramped).
- Mark the chain link that is the true **bottleneck** with ★ — the one cause
  that, if fixed, collapses the rest. Put it in a dashed box.
- Mark **unknown-unknowns** with ◆ — things you can't yet see (unclear buyer,
  unvalidated assumption). Naming them is part of the analysis.
- Mark items needing **escalation** with ▲ — see §2b below. **At least 1,
  ideally 2, root causes across the trees must be ▲.**
- The visual reads: bold problem at the left, "Why-1 → Why-2 → ..." flowing
  right with red labels over blue arrows. Keep each cause to a few words.

## 2b. The escalation test — what "can't solve it myself" means

Run **every root cause** through these five tests. If **any one** hits, the
cause is beyond self-resolution → mark it ▲ and make "ask for help" the
countermeasure. This is the honest version of the analysis: pretending
everything is self-solvable is itself a root cause of failure.

| Test | Question | Typical ▲ example |
|------|----------|-------------------|
| **権限 Authority** | Does fixing it need a decision/approval I can't make (budget, policy, personnel, priorities)? | 標準作業の導入には工場長の決裁が要る |
| **資源 Resources** | Does it need money, tools, data, or access I don't control? | スキャナ購入 ¥80万は部門予算外 |
| **専門知識 Expertise** | Does it need specialist knowledge I can't acquire within the deadline? | 労務規定の解釈は社労士マター |
| **範囲 Scope** | Does the cause live in another team / company / customer's process? | 遅延の起点は顧客の発注プロセス |
| **期限 Deadline** | Could I solve it alone, but not fast enough for the goal? | 独学3か月 vs 外部研修2週間 |

Escalation targets, in rough order of cost: direct boss → senior colleague /
other department → vendor or paid service → external expert (consultant,
士業) → public support (subsidies, 支援機関) → community / network.

An ▲ node is only finished when its countermeasure (section 6) states
**誰に・何を・いつまでに** — who to ask, what exactly to ask for, by when.

---

## 3. Deep-Analysis knowledge patterns

Apply whichever fit. These are what make section 5 expert rather than generic.

**Attention & motivation** (procrastination / drift):
- Top-down: connect today's task to a large future goal ("this supports the
  ¥15M job target").
- Bottom-up: remove immediate temptations from the environment ("no YouTube
  9:00–19:00; phone in another room").
- If-Then planning: convert intention into automatic behavior ("if it's 9:00,
  open the editor and run yesterday's test first").
- Critical-path focus: ship the one thing that unlocks the next step.

**Human factors / vigilance** (monitoring tasks):
- Humans are weak at long-duration vigilance.
- Automate detection/logging to cut the monitoring burden.
- AI supports human review; it does not remove human responsibility.

**AI safety** (LLM/AI in the loop):
- AI output is a draft, not a final answer.
- Add human-in-the-loop review and explicit checkpoints.
- Watch for automation bias; keep responsibility boundaries clear.

**Business translation** (small/personal demo → business value):
- Cat-food loss → factory material loss
- Pet-area stay → worker hazard-zone stay
- Water/toilet logs → behavior monitoring & anomaly detection
- Home camera → low-risk private-data proof of concept

---

## 4. Job-hunt A3 pattern (worked template)

When the theme is job hunting, this is a strong starting structure.

**Center problem:** "The probability of reaching the target job/income within
the deadline is not yet high enough."

**Common cause chains (trees):**
1. *Evidence gap* — demo incomplete, GitHub/portfolio not ready, weak 3rd-party proof.
2. *Age / perception risk* — fit worries, looks too academic, looks expensive,
   weak implementation proof.
3. *Access gap* — not reaching decision-makers, no direct proposal route, no
   shareable proof asset.
4. *Critical-path failure* ★ — too many learning themes/demos competing with the
   main goal; learning replaces shipping. (Often the bottleneck.)
5. *Unknown-unknowns* ◆ — unclear buyer, demo may not translate to business
   value, employer can't imagine where to place the candidate.

---

## 5. Checklists

**Before generating, confirm:**
- [ ] Enough real substance gathered (don't generate from a vague one-liner)
- [ ] Each section reviewed with the user (unless they said "just generate")
- [ ] The Five-Whys reaches actionable roots; the bottleneck is marked ★
- [ ] Every root cause was run through the 5 escalation tests (§2b); **≥1
      (ideally 2) root causes are ▲** — or the user confirmed none apply
- [ ] Unknown-unknowns are named ◆
- [ ] Every ★/▲/◆ maps to a countermeasure; every ▲ countermeasure names
      誰に・何を・いつまでに (who / what / by when)
- [ ] Deep Analysis adds insight beyond the user's own words, **including a
      web-researched escalation-help entry for each ▲**
- [ ] Countermeasures are executable this week
- [ ] Cost includes time and attention, not only money
- [ ] Goals contain numbers (KPI / % / deadline)
- [ ] Timeline has concrete deliverables **and ≥1 verification milestone
      where the Goal KPI is measured (PDCA の Check)**
- [ ] `python scripts/validate_spec.py spec.json` prints no `[WARN]`
- [ ] Content is lean enough to fit each section at the fixed 13 pt body size
      (rebuild and check stderr — shorten any section that warns `[overflow]`)

Ask: *"これでA3シートを作ってよいですか? / Shall I build the A3 now?"*

**After generating, confirm:**
- [ ] Provide the .pptx path and a preview image
- [ ] Nothing clipped at the fixed sizes (body 13 pt, headers 16 pt, flowchart
      12 pt); check cost + sections 5–6 especially
- [ ] Layout is readable and the reading path is obvious

Ask: *"これでいいですか? Deep Analysis / Five-Whys / 文字サイズ / 余白を
さらに改善しますか? — Anything to refine?"*

---

## 6. Iteration pattern (No.2, No.3 …) — the loop is the method

A single A3 is a hypothesis; the loop is the science. When the user confirms
"前回の続き", build the next sheet like this.

**6a. Interview the previous countermeasures one by one.** For each item:
やった？(実施) → どうだった？(効果 vs KPI) → なぜうまくいった／失敗した？
→ 新しい気づきは？ Never accept "実施済" as success — implementation and
effect are different columns.

**6b. Open with the Check table (section 2).** Put `"table"` inside
`current_problems`; the builder renders it under the items. Columns:
前回の施策 / 実施 / 効果. Judge with:

| 記号 | 意味 |
|------|------|
| ◎ | 実施し、KPIに効果が出た |
| ○ | 実施した。効果は観察継続中 |
| △ | 部分的に実施／部分的な効果 |
| × | 未実施 |
| － | 判定不能（データ不足） |

**6c. No silent drops — especially ▲.** Every previous item now
未実施/保留/中止 needs a written reason **and a re-trigger condition**
("口論が月2回 or 過熱1回 → 48時間以内に予約"). One good week is not proof
the system is fixed — "good results = safe to skip" is the too-narrow
definition of safety, and hindsight bias reads a calm period as inevitability.

**6d. Update the Five-Whys as tested hypotheses.** Root causes are chosen,
not discovered — so each cycle re-chooses using the new data. Confirmed
causes stay; refuted ones are replaced; the incident that *still* happened
this cycle gets its own tree. The ★ usually moves: the old bottleneck was
treated, find the next one.

**6e. Graduate what worked (SDCA / 歯止め).** Effective (◎) measures leave
section 6: standardize/automate them (reminders, physical changes, routines
that don't depend on memory or willpower) and record them as 定着済み in the
background. Countermeasures is for the next moves, not a museum.

**6f. Number and link.** Title carries （No.N）; header date = review date;
background recaps the previous cycle in one line. Ask the next review date
(3日後/来週/1か月/1年 — match the KPI's measurement window) and end the new
timeline on "No.N+1 レビュー".
