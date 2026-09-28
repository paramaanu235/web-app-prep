# Google L4/L5 SWE Interview Plan — 12 Weeks

**Calibration first:** With 5 YOE backend, you are a **strong L4** and a **stretch L5**. Default to interviewing as **L5**; HC can downlevel to L4. Do not self-downlevel. Interview **DSA in Python** (speed + stdlib). Keep Java for design/LLD talk.

---

## 1. Level Calibration & Loop

### Typical onsite (5 YOE, L4/L5)

| Round | Count | What “Hire” looks like |
|---|---|---|
| Coding (DSA) | 2–3 × 45 min | Medium+Hard, talking while coding, tests, complexity |
| System Design | 1 × 45 min | L4: correct components. L5: tradeoffs, failure modes, scale, ownership |
| Googleyness & Leadership | 1 × 45 min | Ambiguity, conflict, impact, collaboration — not “culture fit fluff” |
| Sometimes | +1 coding or domain | Extra coding if mixed; skip extra design unless L5+ |

Phone/virtual screen is usually **1 coding** before the full loop.

### L4 vs L5 (what HC actually scores)

| Dimension | L4 (SWE III) | L5 (Senior) |
|---|---|---|
| Scope | Feature / service slice | Multi-service system, 6–18 month horizon |
| Design | Uses known patterns correctly | Drives API/data-model/consistency choices and defends them |
| Coding | Clean, correct, O-optimal | Same, plus structure that would survive production |
| Ambiguity | Asks clarifying Qs | **Reduces** ambiguity; states assumptions; proceeds |
| Leadership | Mentors juniors informally | Influences without authority; pushback with data |
| Failure | Owns bugs | Owns *systems* of failure (process, design, rollout) |

**L5 bar in coding:** not harder LeetCode. It’s **communication, correctness under pressure, and not needing hints**. In design, L5 is expected to lead the conversation.

### Python vs Java for DSA

**Use Python.** Reasons:

- 40–50% less typing in 45 min
- `heapq`, `collections.deque/Counter/defaultdict`, `bisect`, slicing, unpacking
- Interviewers care about algorithms, not Spring
- Use Java only if you freeze in Python under pressure (you won’t after week 4)

**Python interview kit (memorize):**
`deque`, `heapq`, `defaultdict`, `Counter`, `bisect`, `set`, `dict`, list/set comprehensions, `sys.setrecursionlimit` if needed. Know `ListNode`/`TreeNode` from scratch.

---

## 2. 12-Week Roadmap (15–20 h/week)

**Totals:** ~200 hours. Split ≈ **55% DSA / 25% Design / 15% Behavioral / 5% mocks & review**.

### Weekly template (lock this)

| Slot | Time | Work |
|---|---|---|
| Mon–Thu | 2 h | 1 timed problem (35 min) + 25 min solution review / pattern notes |
| Fri | 2 h | Weak-pattern drill **or** 1 design sketch |
| Sat | 4–5 h | 2 problems (1 Hard) + 1 full design (45 min writeup) |
| Sun | 3–4 h | Behavioral STAR (1 h) + spaced review of missed problems + light coding |

**Daily coding ritual (non-negotiable):** 2 min restatement → 3 min examples → brute force → complexity → code → 3 edge cases → time/space. Never “just code.”

---

### Phase 1 — Weeks 1–4: Foundations & Patterns (~70 h)

**Goal:** Instant recognition of Google-heavy patterns. Mediums in 20–25 min without hints.

| Week | Focus | Hours | Milestone (must hit) |
|---|---|---|---|
| **1** | Arrays, Hashing, Two Pointers, Sliding Window, Intervals | 16–18 | 18 Mediums. Merge Intervals / subarray sum / anagrams cold. |
| **2** | Binary Search (incl. answer-space), Heap, Intervals+, Greedy | 16–18 | 15 Medium + 3 Hard. Binary search template from memory. |
| **3** | Trees, BST, Recursion, Tries | 16–18 | LCA, serialize, trie prefix/wildcard. Recursion → iterative when asked. |
| **4** | Graphs: BFS/DFS, Topo sort, Union-Find, Grid | 18–20 | Course schedule, number of islands, accounts merge, shortest path **unweighted**. Timed 2×45 min mock. |

**Phase 1 exit bar:** 60–70 LeetCode (mostly Medium). Any Medium in these patterns in ≤25 min. Pattern notebook: 1 page per pattern (template + 3 pitfalls).

---

### Phase 2 — Weeks 5–8: Hard DSA + System Design (~70 h)

**Goal:** Hards don’t panic you. You can run a 45-min Google-style design.

| Week | DSA | Design | Milestone |
|---|---|---|---|
| **5** | DP 1: 1D/2D, knapsack, LIS, string DP | CAP, replication, sharding, consistent hashing | 12 DP Medium + 3 Hard. Can explain leader/follower vs multi-leader. |
| **6** | DP 2: interval DP, bitmask intro, tree DP (light) | Caching, CDN, rate limiting, idempotency | Design **URL shortener** + **rate limiter** end-to-end. |
| **7** | Graphs hard: Dijkstra, 0-1 BFS, bipartite, SCC (light) | Queues, pub/sub, exactly-once vs at-least-once, Bigtable vs SQL | Design **News feed** or **Task queue**. Map to Pub/Sub + Bigtable in your stories. |
| **8** | Combined: graphs+DP, tries+DFS, sweep line | BigQuery/analytics path, data models, secondary indexes | Design **YouTube-like** or **Gmail-like**. 2 timed coding mocks. |

**Phase 2 exit bar:** ~110–130 problems total. 25–30 Hards touched (not all mastered). 4 design writeups you can redraw in 40 min.

---

### Phase 3 — Weeks 9–12: Mocks, Speed, HC Polish (~60 h)

**Goal:** Interview-shaped performance. No new patterns after week 10.

| Week | Focus | Milestone |
|---|---|---|
| **9** | 4 timed coding (45 min) + 2 designs. Start story bank dry-runs. | Coding: finish with tests 4/5 times. |
| **10** | Weakest 2 patterns only. 3 mocks (mix coding/design). Behavioral 5 stories aloud. | Zero “hint needed” on Mediums. |
| **11** | Full loop simulation: 3 coding + 1 design + 1 behavioral in 1 day (Sat). Recovery Sun. | Stamina. Notes on where you went quiet. |
| **12** | Taper: 1 problem/day (review, not new). 2 light mocks. Sleep, logistics, cheat-sheet of complexities + STAR bullets. | Peak, not grind. |

---

## 3. DSA Strategy (Google-heavy, not 500 random)

### Pattern stack (priority order)

1. **Graphs — BFS/DFS / grid / topo** — highest Google density
2. **Binary search on answer**
3. **Heaps + intervals / sweep**
4. **Trees + recursion + LCA**
5. **Union-Find**
6. **DP (1D/2D/string)** — they will ask at least one
7. **Tries / prefix**
8. **Sliding window / two pointers / hashing** (week 1, then maintenance)
9. **Design-flavored coding:** iterators, LRU, snapshot, rate limiter code

Skip: niche bit tricks, heavy geometry, advanced flow, contest-only math — unless a mock exposes a hole.

### Volume target (12 weeks)

| | Count | Notes |
|---|---|---|
| Medium | **90–110** | Core. Must be timed. |
| Hard | **25–35** | Quality > count. Re-solve 1 week later. |
| Easy | **10–15** | Warmup only. |
| **Total** | **~130–150** | Not 500. Re-solve misses until clean. |

**Rule:** If you needed the solution, it doesn’t count until you re-solve it 3–7 days later with no notes.

### Live interview framework (use every time)

1. **Clarify (2–3 min):** input types, duplicates, sorted?, in-place?, scale (n=10^5?), return what on empty. Repeat the problem in one sentence.
2. **Examples (2 min):** 1 normal, 1 edge (empty / 1 element / all same).
3. **Brute force (1–2 min):** say it, complexity, why it fails.
4. **Optimize:** name the pattern (“this is BFS on implicit graph”). Complexity before code.
5. **Code:** helper names, no silent mutations, talk structure not keystrokes.
6. **Test:** your examples + null, overflow, disconnected graph, cycle.
7. **If stuck (5 min):** smaller version, known similar problem, trade time for extra space. **Ask** a directed question, don’t go silent.

**L5 tell:** you propose brute → better → discuss follow-up (“what if stream / disk / concurrent?”) without being asked.

---

## 4. System Design (use your actual stack)

You have a **Google-native data story**. Interviewers notice when design maps to real systems. Use it; don’t recite Alex Xu chapters.

### How to leverage PostgreSQL / Bigtable / BigQuery

| Store | Use when | Say this in the interview |
|---|---|---|
| **PostgreSQL** | Strong consistency, relations, transactions, secondary indexes, OLTP | Payments, user metadata, ACLs. Mention connections, replicas, failover. |
| **Bigtable** | Huge sparse key-value, high write, key-range scans, single-key access | Time-series, activity, messages-by-user. **Row-key design is the interview.** |
| **BigQuery** | Analytics, scan-heavy, not serving path | “Serving = Bigtable/SQL; analytics = export to BQ. Don’t query BQ in the request path.” |

**L5 move:** pick the store from access pattern (read/write QPS, key vs scan vs join, consistency), not from “NoSQL is web scale.”

### Core topics (master, don’t skim)

- CAP / PACELC, consistency models (linearizable, sequential, eventual)
- Replication (leader, multi-leader, quorum) + failover
- Sharding + **consistent hashing** + rebalancing
- Caching (aside, read-through, write-through, stampede, TTL)
- Rate limiting (token bucket, sliding window, distributed)
- Queues vs streams (at-least-once, idempotency keys, poison pills)
- Load balancing, health checks, graceful degradation
- Data modeling: PK, indexes, **Bigtable row keys**, hotspots
- Back-of-envelope: QPS, storage, bandwidth (practice until automatic)

### 5 canonical designs (practice each twice: 45 min + review)

1. **URL shortener** — hashing, 301/302, DB choice, uniqueness
2. **Distributed rate limiter** — your Java/Python services; Redis vs memory; correctness
3. **Google Drive / Docs-lite** — metadata SQL, blobs, notifications, consistency
4. **YouTube / video ingest** — upload, transcode queue, CDN, metadata, Bigtable for views
5. **Analytics pipeline (Search/ads-lite)** — events → Pub/Sub → stream + **BigQuery**; serving vs warehouse split

**Bonus if targeting L5:** **Gmail** or **Maps-ish** (geo sharding) — harder data model.

### Design 45-min skeleton

Requirements (functional + non) 5 → estimates 5 → API + data model 8 → high-level 8 → deep-dive 1–2 bottlenecks 12 → failures/scale 5. **You** drive. L4 waits to be asked; L5 sequences the board.

---

## 5. Googleyness & Leadership

### Top 5 themes they probe

1. **Ambiguity** — incomplete spec, you still shipped
2. **Disagreement / pushback** — you changed a plan *or* were correctly overruled
3. **Cross-functional conflict** — PM/partner/ops, not “my teammate is wrong”
4. **Failure** — production or project; what *you* changed after
5. **Mentorship & raising the bar** — review quality, design docs, unblocking others

Also: ethics/privacy, inclusion (credit, interrupting, hiring), taking a stand vs going along.

### Story bank (5 YOE → 8–10 stories, not 30)

Map **one story per theme**, plus 2 “impact” and 1 “technical depth.”

**STAR+R (Google prefers the last R):**
**S**ituation (2 sentences) → **T**ask (your job, not the team’s) → **A**ction (**70%**, first person, decisions) → **R**esult (metric) → **Reflection** (what you’d repeat / change).

**Mine your background:**

- PostgreSQL: incident, schema migration, deadlock, replica lag
- Bigtable: row-key hotspot, hotspot fix, GC/TTL, query pattern change
- BigQuery: cost explosion, partition/cluster, “don’t put this on the serving path”
- Django/FastAPI/Spring: API contract fight, versioning, latency SLO

Write **bullet STAR cards** (not scripts). Practice aloud 8 min each. Never bash a company or a person.

---

## 6. Resources (high-signal only) & HC pitfalls

### Resources

| Need | Use |
|---|---|
| Patterns | **Grokking / NeetCode 150** as *index*, not as the course. Your list above. |
| Problems | LeetCode; filter Google tag **after** patterns, not instead of. |
| Coding mocks | **interviewing.io** or **pramp**; 6+ paid/peer mocks weeks 9–11. Human > GPT. |
| Design | **Alex Xu Vol 1** (selected ch.) + **System Design Interview** practice. Your 5 problems. **DDIA** chapters: replication, partitioning, consistency — not the whole book. |
| Behavioral | Your story bank + “Googleyness” interview questions lists. Record yourself. |
| Language | Python `collections` / `heapq` docs. One cheat sheet. |

Skip: grinding 500 Easy, random YouTube daily, buying 4 design courses.

### 5 mistakes that kill you at HC (even with working code)

1. **Silent coding** — HC packet has no evidence of reasoning. Talk or it didn’t happen.
2. **No tests / no complexity** — “it passed the example” is Insufficient.
3. **Hint-dependent** — working solution after 3 hints = L3/L4 lean, not L5.
4. **Design as a component list** — boxes without QPS, data model, failure, or *why Postgres vs Bigtable*.
5. **Behavioral generic / no “I”** — “we shipped a microservice.” HC cannot assign *you* credit. Also: blaming others, or zero conflict stories (looks junior).

**Honorable mention:** interviewing in Java and running out of time; overselling L5 while stories are L4 scope (feature work only).

---

## Immediate next 7 days

- Decide **Python** for coding; set LeetCode + timer.
- Week 1 list: Two Sum family, sliding window max, merge intervals, subarray sum equals K, longest substring without repeat, 3Sum, product except self, container with most water.
- Draft 8 STAR titles (one line each) from Postgres/Bigtable/BQ incidents.
- Book **first mock for end of week 4** now (calendar makes the rest real).

**L4/L5 call at week 8:** if timed Hards still need hints and design is “list of services,” go in as L4-ready with L5 stretch. If you lead design and finish 2 Mediums or 1 Hard clean, push L5.

Track weekly: problems timed vs untimed, mocks, stories practiced. If a week slips, cut volume — **never cut timed practice or story rehearsal.**
