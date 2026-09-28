# STAR Story Bank — Google 5 YOE

Use STAR+R: Situation → Task → Action → Result → Reflection.

Write these from your real backend experience (PostgreSQL, Bigtable, BigQuery, Django/FastAPI, Spring Boot).

---

## 1. Ambiguity

**Situation:** (project, unclear scope)  
**Task:** (your specific job)  
**Action:** (how you reduced ambiguity — asked, proposed, decided, set)  
**Result:** (metric)  
**Reflection:** (what you'd repeat)

Example skeleton — **fill with your real project**:
> On a BigQuery analytics migration, the data model was undefined and stakeholders had conflicting SLAs. I drove a 1-week alignment: defined event schemas, partitioning strategy, and query budgets. Shipped 3 weeks early with 40% cost reduction. I'd repeat the schema-first approach.

---

## 2. Disagreement / Pushback

**Situation:** (technical disagreement with PM, peer, or leadership)  
**Task:** (your position)  
**Action:** (how you pushed back with data, or accepted and delivered)  
**Result:** (what changed)  
**Reflection:**

> A PM wanted to ship a BigQuery query to the serving path. I showed query-time and concurrency numbers; we moved to an async materialized view. Query went from 12s to 200ms. I'd do the same pushback again.

---

## 3. Cross-functional collaboration

**Situation:** (PM, designer, ops, data eng, etc.)  
**Task:** (your role bridging teams)  
**Action:** (how you aligned)  
**Result:** (delivered)  
**Reflection:**

---

## 4. Failure / production incident

**Situation:** (what broke)  
**Task:** (your responsibility)  
**Action:** (what you did, owned, fixed)  
**Result:** (time to restore, what changed)  
**Reflection:**

> Deadlocks in PostgreSQL under load during a schema migration. I owned the postmortem, added retry + exponential backoff, and introduced a migration gate. Post-incident query latency dropped 60%. I'd have flagged the lock timeout earlier in design.

---

## 5. Mentorship / raising the bar

**Situation:** (junior joining, code quality, review culture)  
**Task:** (your role)  
**Action:** (what you did)  
**Result:** (impact)  
**Reflection:**

---

## 6. Impact / ownership (project shipped)

**Situation:** (what you built)  
**Task:** (your scope)  
**Action:** (how you delivered)  
**Result:** (metrics — latency, cost, throughput, users)  
**Reflection:**

---

## 7. Impact 2 (second project, different domain)

Same skeleton. Different domain (analytics, infra, migration, performance).

---

## 8. Technical depth (hard problem)

**Situation:** (tough technical problem — query optimization, distributed system, data model)  
**Task:** (solve it)  
**Action:** (deep technical reasoning)  
**Result:** (numbers)  
**Reflection:**

> Optimized a BigQuery ETL from 45 min to 8 min: partitioned by ingestion date, clustered on user_id, replaced nested loops with window functions. Saved $24k/month in compute.

---

## STAR rules

1. **First person, present tense** ("I led", not "we").
2. **Metric in every story** (time, cost, %, users).
3. **Never blame** a company, team, or person.
4. **Keep to 3–4 min** per story when told aloud.
5. **Prepare 2 versions**: one 60s (resume) + one 3min (full).
6. **Rehearse aloud** 8 min each. Record yourself.
7. **Never say** "I don't have a story for that." Pick the closest theme.

---

## Theme quick map

| Theme | Pick a story about... |
|---|---|
| Ambiguity | undefined spec, you shipped anyway |
| Disagreement | you changed a plan or were overruled |
| Cross-functional | PM/ops/data eng conflict you resolved |
| Failure | production bug; what you changed |
| Mentorship | unblocking a junior; review quality |
| Impact | shipped feature with metrics |
| Technical depth | hard optimization / data model / distributed |

---

## Prep this week (do now)

1. Fill in all 8 tables with **real** projects from your backend experience.
2. Pick your 5 strongest stories — those are your interview anchors.
3. Time each aloud. Trim to ≤ 3 min.
4. Record one full run-through. Listen for "um" and vagueness.
