# Quick reference — all files at a glance

## Files in this prep directory

| File | What it covers |
|---|---|
| `grok_proposed_plan.md` | 12-week L4/L5 roadmap, DSA/design/behavioral breakdown |
| `grok_coding_questions.md` | ~140 LeetCode problems grouped by week/pattern |
| `grok_python_snippets.md` | Python muscle memory: 25 sections, running examples |
| `java_interview_cheatsheet.md` | Java DSA: 53 snippets, compilation tested |
| `java_design_pattern_cheatsheet.md` | 34 design patterns with running Java examples |
| `java_8_vs_17_interview_guide.md` | Language diffs, demoted/deprecated patterns, migration traps |
| `fastapi_cheatsheet.md` | FastAPI 0.141.1 + Pydantic v2 |
| `django_cheatsheet.md` | Django 6.1 (LTS 5.2) |
| `spring_boot_cheatsheet.md` | Spring Boot 4.1.1, Framework 7.0.9 |
| `amazon_dsa_questions.md` | ~120 Amazon-recurring problems, OA + onsite |
| `weekly_tracker.md` | Fill-in tracker, mock log, story bank skeleton |
| `star_story_bank.md` | STAR+R templates for all 8 themes |
| `quick_reference.md` | This file |

## Interview language decision

**DSA rounds:** Python. `deque`, `heapq`, `defaultdict`, `Counter`, `bisect`.
**Design rounds:** Java. Spring Boot / Postgres / Bigtable / BigQuery story bank.

## 12-week rhythm (15–20 h/week)

| Phase | Weeks | Focus | Hours |
|---|---|---|---|
| Foundations | 1–4 | Arrays/hash/BS/heap/trees/graphs/DP I | ~70 |
| Advanced | 5–8 | DP II/hard graphs/design/Bigtable/BigQuery | ~70 |
| Mocks | 9–12 | Timed coding, design, STAR, no new patterns | ~60 |

## Design patterns to lead with (L5 tell)

Strategy (lambdas) · Decorator (IO streams) · Observer (pub/sub) · Builder (optional fields) · Adapter (legacy API) · Facade (hide subsystem) · Singleton (enum) · DI (constructor) · State (lifecycle objects) · Sealed + pattern matching (closed ASTs)

## Design stores mapping (use in interviews)

| Store | When | Say this |
|---|---|---|
| PostgreSQL | strong consistency, relations, OLTP | "transactions, replicas, failover" |
| Bigtable | sparse key-value, high write | "row-key design is the interview" |
| BigQuery | analytics, scan-heavy | "never in the request path" |

## Top 5 HC kill mistakes

1. Silent coding — talk or it didn't happen
2. No tests / no complexity stated
3. Hint-dependent — after 3 hints = L3 lean
4. Design = boxes without QPS / failure mode
5. Behavioral = "we" with no "I"

## Weekly check (Sunday, 5 min)

- [ ] ≥ 12 h logged? Else cut scope, not timing
- [ ] ≥ 1 mock by week 9? Else cancel a design session
- [ ] ≥ 3 story rehearsals this week? Else add 30 min Sunday slot
- [ ] Slow-pattern list reviewed? Else add one re-solve
- [ ] One design redraw from memory? If not, schedule Saturday slot

## Immediate next 7 days

1. Commit to **Python** for DSA. `uv add "fastapi[standard]"`.
2. Week 1 problems: 1, 3, 11, 15, 42, 49, 53, 56, 57, 75, 76, 128, 167, 209, 217, 238, 239, 242, 283, 347, 424, 435, 438, 560, 567 + LL: 2, 19, 21, 25, 138, 141, 143, 148, 206
3. Fill STAR story bank tables **today** (8 stories from real projects).
4. Book mock for **end of week 4** (calendar makes it real).
5. Read `grok_python_snippets.md` section 25 drill (12 templates from blank).
