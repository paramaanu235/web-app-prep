# Google SWE Interview Preparation Plan (12-Week Roadmap)

**Target Level:** Google L4 (SWE III) / L5 (Senior SWE)  
**Candidate Profile:** 5 Years Experience | Backend (Python, Java) | PostgreSQL, Bigtable, BigQuery  
**Time Commitment:** 15–20 hours/week (~2 hrs weekdays, 4–5 hrs weekends)  
**Timeline:** 12 Weeks (~3 Months)

---

## Part 1: Level Calibration & Interview Rounds Breakdown

### 1. The Interview Loop for a 5 YOE Candidate
At Google, a candidate with 5 years of experience is in the **L4 / L5 fungible bracket**. Recruiters calibrate the loop based on your pre-screen and target:
* **Coding Rounds (3 rounds, 45 mins each):** Data structures, algorithmic problem solving, clean code, time/space complexity analysis, and edge-case handling.
* **System Design Round (1 or 2 rounds, 45 mins each):**
  * *L4 standard loop:* 3 Coding + 1 System Design (HLD) + 1 Googleyness & Leadership (G&L).
  * *Targeted L5 loop:* 2 Coding + 2 System Design (or 3 Coding + 1 HLD + 1 G&L, where an exceptional performance in HLD and G&L triggers L5 consideration at Hiring Committee).
* **Googleyness & Leadership (1 round, 45 mins):** Behavioral evaluation focused on navigating ambiguity, cross-functional collaboration, ownership, and psychological safety.

---

### 2. L4 vs. L5 Rubric Calibration

| Dimension | L4 (Software Engineer III) | L5 (Senior Software Engineer) |
| :--- | :--- | :--- |
| **Problem Solving (GCA)** | Solves well-scoped, complex problems. Reaches optimal solution with minor hints. | Navigates underspecified, ambiguous problems. Proactively clarifies scope, proposes alternatives, and evaluates non-trivial trade-offs. |
| **Code Quality & Speed** | Writes correct, idiomatic code in ~30 mins. Handles standard edge cases. | Writes production-grade, modular, easily extensible code in ~20–25 mins. Identifies obscure edge cases without prompting. |
| **System Design** | Designs scalable architectures using standard patterns (load balancers, caches, sharding). Identifies single points of failure. | Evaluates nuanced trade-offs (consistency vs. latency, write-amplification, failure modes). Drives capacity planning, API contracts, monitoring, and DR strategy. |
| **Leadership / Impact** | Reliable self-starter. Collaborates well within the team. Executes independently. | Multiplies team impact. Resolves cross-team friction, mentors juniors, sets technical direction, and exhibits resilience post-failure. |

> [!IMPORTANT]
> **The Hiring Committee (HC) Rule for L5:** You cannot be upleveled to L5 purely on coding scores. L5 requires **demonstrated technical breadth and leadership maturity** in both the System Design and G&L rounds, combined with strong coding rounds.

---

### 3. Language Strategy: Python vs. Java
**Verdict: Interview in Python for Coding/DSA.**

* **Speed & Brevity:** In a 45-minute Google interview, you have only **25–30 minutes of active coding time** (after 5–7 mins of clarification and before 5–10 mins of dry-running and follow-ups). Java’s boilerplate (verbose class declarations, getters/setters, verbose generic types) costs 5–8 minutes of typing and syntax friction.
* **Standard Library Advantage:** Python’s `collections.deque`, `heapq`, `defaultdict`, `Counter`, and list comprehensions let you express complex graph and heap logic in 3–4 lines where Java requires 15–20 lines.
* **Caveats to Master in Python:**
  1. `heapq` is a min-heap by default; know how to invert values for max-heap or wrap elements as `(priority, item)`.
  2. Understand the time complexities of standard operations (e.g., `list.pop(0)` is $O(N)$, `deque.popleft()` is $O(1)$; slicing `a[1:]` creates an $O(K)$ shallow copy).
  3. Be prepared to implement custom comparator classes or keys for sorting when tuples are insufficient.
* **Where Java Shines:** If an interviewer asks an Object-Oriented or Low-Level Design (LLD) question, you can offer Java. For all DSA rounds, use Python.

---

## Part 2: 12-Week Milestone-Driven Roadmap

```
Phase 1 (Weeks 1–4)   ──► Foundations, Core Patterns & Design Primitives (18 hrs/wk)
Phase 2 (Weeks 5–8)   ──► Advanced Algorithmic Patterns & Scaled Architectures (18 hrs/wk)
Phase 3 (Weeks 9–12)  ──► Timed Mocks, Speed Optimization & Polish (15-18 hrs/wk)
```

### Weekly Schedule Template (~17 Hours/Week)
* **Monday – Thursday (2 hrs/day = 8 hrs):**
  * *60 mins:* Solve 1–2 focused DSA problems under a 25-minute timer.
  * *60 mins:* System design reading / distributed systems concepts or DSA pattern review.
* **Friday (1 hr):** Active recall: Re-solve 1 problem you struggled with earlier in the week from scratch.
* **Saturday (4 hrs):**
  * *2 hrs:* Deep-dive System Design end-to-end problem (diagramming, calculations, bottleneck analysis).
  * *2 hrs:* 2 Hard DSA problems on current weekly pattern.
* **Sunday (4 hrs):**
  * *1.5 hrs:* Mock Interview (peer on Pramp/Interviewing.io or self-recorded under strict 45-minute timer).
  * *1.5 hrs:* Review mock, log mistakes into an "Error Log".
  * *1 hr:* Draft / rehearse 1 behavioral STAR story.

---

### Phase 1: Foundations, Patterns & Building Blocks (Weeks 1–4)

#### Week 1: Arrays, Two Pointers, Sliding Window & Math
* **DSA Focus:** Two pointers, sliding window (fixed & dynamic), prefix sums, Kadane's algorithm.
* **System Design Focus:** Back-of-the-envelope calculations (QPS, storage, bandwidth), latency numbers every programmer should know, networking basics (TCP vs. UDP, HTTP/2, gRPC).
* **Weekly Target:** 10 Mediums, 2 Hards.

#### Week 2: Graphs I (BFS, DFS, Matrix Traversal, Flood Fill)
* **DSA Focus:** Grid traversals, connected components, cycle detection in directed & undirected graphs, multi-source BFS.
* **System Design Focus:** Relational (PostgreSQL) vs. Distributed NoSQL (Bigtable) deep dive: Storage engines (B-Tree vs. LSM-Tree), ACID vs. BASE.
* **Weekly Target:** 10 Mediums, 2 Hards.

#### Week 3: Graphs II (Topological Sort, Dijkstra, Union-Find)
* **DSA Focus:** Kahn’s algorithm, cycle detection in DAGs, Disjoint Set Union (DSU with path compression & union by rank), Dijkstra’s algorithm.
* **System Design Focus:** Horizontal Partitioning & Sharding, Consistent Hashing (virtual nodes), Replication strategies (Leader-Follower, Quorum $R+W>N$).
* **Weekly Target:** 8 Mediums, 3 Hards.

#### Week 4: Heaps, Intervals & Binary Search Variations
* **DSA Focus:** Top-K problems, merge intervals, interval intersections, Binary Search on continuous/discrete answer spaces ("Min of Max").
* **System Design Focus:** Caching patterns (Cache-Aside, Write-Through, Write-Behind, Eviction policies: LRU/LFU), Cache stampede mitigations.
* **Weekly Target:** 10 Mediums, 2 Hards.

> [!TIP]
> **Phase 1 Milestone:** 45+ LeetCode Medium/Hard problems solved; can implement BFS/DFS, Union-Find, and Topological Sort from memory in $<12$ minutes without reference.

---

### Phase 2: Advanced Topics & System Scaling (Weeks 5–8)

#### Week 5: Dynamic Programming I (1D & Knapsack Variants)
* **DSA Focus:** Memoization vs. Tabulation, decision trees, House Robber, Coin Change, Word Break.
* **System Design Focus:** Asynchronous processing: Message Queues (RabbitMQ) vs. Event Streams (Kafka/Google Pub/Sub), delivery guarantees (at-least-once, exactly-once via idempotency keys).
* **Weekly Target:** 8 Mediums, 3 Hards.

#### Week 6: Dynamic Programming II (2D/Grid, Subsequences, Strings)
* **DSA Focus:** Longest Common Subsequence, Edit Distance, Longest Increasing Subsequence ($O(N \log N)$ approach), Grid path DP.
* **System Design Focus:** Case 1: *Design a Globally Distributed Key-Value Store* (leveraging Bigtable knowledge: SSTables, MemTable, WAL, Compactions).
* **Weekly Target:** 7 Mediums, 3 Hards.

#### Week 7: Tries, Monotonic Stacks & String Algorithms
* **DSA Focus:** Trie implementation with prefix matching, Monotonic Stack (Next Greater Element, Daily Temperatures, Largest Rectangle in Histogram).
* **System Design Focus:** Case 2: *Design a Metrics & Time-Series Monitoring Platform* (leveraging Bigtable for write-heavy ingestion and BigQuery for analytical slicing).
* **Weekly Target:** 8 Mediums, 3 Hards.

#### Week 8: Backtracking, Trees & System Design Integration
* **DSA Focus:** N-Queens, Subsets/Permutations pruning, Lowest Common Ancestor, Tree serialization/deserialization.
* **System Design Focus:** Case 3: *Design YouTube / Video Ingestion and Transcoding Pipeline* (Blob storage, async worker queues, CDN caching).
* **Weekly Target:** 8 Mediums, 2 Hards.

> [!TIP]
> **Phase 2 Milestone:** 90+ total problems completed. System design blueprints completed for 3 canonical architectures with explicit capacity estimations and failure analysis.

---

### Phase 3: Mocks, Speed, Googleyness & Polish (Weeks 9–12)

#### Week 9: Timed Problem Solving & Proximity Design
* **DSA Focus:** Google-tagged LeetCode problems (last 6 months), strict 25-minute timer per problem.
* **System Design Focus:** Case 4: *Design a Proximity Service / Google Places* (Geohashing, QuadTrees, S2 Geometry).
* **Mocks:** 2 live coding mocks.

#### Week 10: Mixed Hard Problems & G&L Story Bank Finalization
* **DSA Focus:** Multi-pattern combinations (e.g., Graph + Heap, DP + Tree).
* **Behavioral Focus:** Finalize 5 core STAR stories across all Google competency pillars. Conduct 1 G&L mock.
* **Mocks:** 1 System Design mock + 1 Coding mock.

#### Week 11: Full Interview Loop Simulation
* **Simulation Day:** Run back-to-back sessions on a weekend:
  * Round 1: DSA (45 min)
  * Round 2: DSA (45 min)
  * Round 3: System Design (45 min)
  * Round 4: Googleyness & Leadership (45 min)
* Review recordings / notes; identify pacing or communication bottlenecks.

#### Week 12: Deliberate Tapering & High-Signal Review
* **Activity:** No new Hard problems. Review your "Error Log", re-read core chapters of *Designing Data-Intensive Applications*, practice code dry-running on a whiteboard or plain text editor (no IDE auto-complete).
* Rest 48 hours prior to interview day.

---

## Part 3: Data Structures & Algorithms (DSA) Strategy

### 1. Google-Heavy Patterns (Ranked by Frequency)
Google interviewers avoid standard textbook problems in favor of multi-layered, graph-centric, or stream-based challenges:

1. **Graphs (BFS/DFS, Topological Sort, DSU, Dijkstra):** Represents ~35% of Google rounds.
   * *Variations:* Multi-source BFS (e.g., rotting oranges, walls and gates), cycle detection in directed state spaces, dynamically connected components using Union-Find.
2. **Intervals & Sweep-line:**
   * *Variations:* Meeting rooms II, non-overlapping intervals, interval list intersections, coordinate compression.
3. **Tries & Prefix Trees:**
   * *Variations:* Autocomplete search, word search II with Trie pruning, file system directory path searches.
4. **Binary Search on Solution Space:**
   * *Pattern:* Identifying monotonicity where the output is unknown but validating a candidate solution takes $O(N)$ (e.g., Split Array Largest Sum, Koko Eating Bananas).
5. **Dynamic Programming (State Transitions):**
   * *Focus:* Google favors memoized DFS or state-machine DP (stock trading with cooldown/fees, knapsack extensions) over obscure 3D DP.
6. **Monotonic Stack / Queue:**
   * *Pattern:* Finding immediate smaller/larger elements in $O(N)$ (e.g., Trapping Rain Water, Largest Rectangle in Histogram).

---

### 2. Target Problem Distribution
* **Total Target:** **120–130 problems** (Quality, variety, and spaced repetition beat raw volume).
  * *Easy:* ~10 (Only for warm-ups when learning a new pattern).
  * *Medium:* **~85–90 (70%)** — The benchmark Google coding question.
  * *Hard:* **~30 (25%)** — Often presented as the "Follow-up" extension to a Medium problem during the live round.

---

### 3. The 5-Step Live Interview Framework (45-Minute Breakdown)

```
[00:00 - 05:00]  Step 1: Clarification, Constraints, & Edge Cases
[05:00 - 12:00]  Step 2: Brute Force -> Optimal Approach & Complexity Pitch
[12:00 - 30:00]  Step 3: Clean, Modular Implementation (Think Aloud)
[30:00 - 40:00]  Step 4: Manual Dry Run & Self-Verification (Find your own bugs)
[40:00 - 45:00]  Step 5: Follow-Up Questions, Scaling, & Big-O Defense
```

* **Step 1: Clarification & Constraints (0–5 min):**
  * Never write code immediately.
  * Ask: *"Can the input array contain negatives or duplicates?", "How large is $N$? Will it fit in memory?", "What should we return if the input is empty or invalid?"*
  * Write a sample input/output test case on screen.
* **Step 2: Approach & Verification (5–12 min):**
  * State the brute-force baseline: *"The brute-force is $O(N^2)$ by checking every pair. We can do better."*
  * Pitch the optimal solution with trade-offs: *"By using a min-heap, we can improve time to $O(N \log K)$ with $O(K)$ space."*
  * **The Checkpoint:** Ask: *"Does this approach sound good to you, or would you like me to consider another angle before I begin coding?"*
* **Step 3: Clean Implementation (12–30 min):**
  * Write modular code. Extract sub-logic into helper functions (e.g., `def get_neighbors(node):`).
  * Use descriptive variable names: `visited_nodes`, `indegree_map`, not `v`, `m`, `arr2`.
  * Maintain running commentary explaining *why*, not just *what*.
* **Step 4: Dry Run & Edge Cases (30–40 min):**
  * **Do not say "I'm done" or ask "Should I run it?"**
  * Pick your sample test case. Step through each line of code, manually updating variable states in comments.
  * Check boundaries: $N=0$, $N=1$, sorted, reverse-sorted, all identical elements.
  * *Scoring secret:* Finding and fixing your own bug during a dry run earns positive points; waiting for the interviewer to point it out incurs a penalty.
* **Step 5: Analysis & Follow-Up (40–45 min):**
  * State Time and Space complexity cleanly using formal notation (e.g., Time: $O(V + E)$, Space: $O(V)$ auxiliary recursion stack).
  * Answer the inevitable follow-up: *"What if the input is a stream that doesn't fit on a single machine?"*

---

## Part 4: System Design (HLD) Strategy

### 1. Leveraging Your Specific Tech Stack (PostgreSQL, Bigtable, BigQuery)
Google interviewers love candidates who possess deep, production-tested knowledge of distributed primitives rather than superficial buzzwords. Use your stack deliberately:

* **Google Cloud Bigtable (Wide-Column NoSQL):**
  * *Where to apply:* High-throughput write workloads, time-series telemetry, user clickstreams, chat message stores, real-time analytics ingestion.
  * *Demonstrate Depth:* Discuss **Row-Key design** to prevent tablet hot-spotting (e.g., salting keys, hashing user IDs, prefixing timestamps with entity IDs). Explain how LSM-trees work (MemTable $\to$ Commit Log $\to$ SSTables on Colossus), and why Bigtable excels at sequential reads/writes but lacks multi-row ACID transactions.
* **PostgreSQL (Relational / ACID):**
  * *Where to apply:* Financial transactions, user authentication/profile management, inventory tracking, order ledgers where strict ACID guarantees and complex relational integrity are required.
  * *Demonstrate Depth:* Explain how you scale Postgres: Read replicas with asynchronous replication lag considerations, connection pooling (PgBouncer), partitioning (declarative range/hash), and horizontal sharding strategies.
* **BigQuery (Analytical Warehouse / OLAP):**
  * *Where to apply:* Decoupling OLTP from OLAP. Asynchronous event ingestion from message brokers into BigQuery for reporting, machine learning feature stores, audit logging, and heavy aggregation queries.
  * *Demonstrate Depth:* Contrast row-oriented storage with columnar storage (Capacitor format); discuss partition pruning and clustering to minimize data scanning and query latency.

---

### 2. Core Distributed Systems Topics to Master
1. **Data Partitioning & Sharding:** Range-based vs. Hash-based partitioning; Consistent Hashing with virtual nodes (ring topology, node rebalancing).
2. **Consensus & Replication:** Leader-Follower vs. Leaderless (Dynamo style); Quorum reads/writes ($R + W > N$); Paxos/Raft conceptual awareness.
3. **Consistency Models:** Strong consistency vs. Eventual consistency vs. Read-your-own-writes (Monotonic Read) consistency; PACELC theorem.
4. **Rate Limiting & Traffic Management:** Token Bucket, Leaky Bucket, Sliding Window Counter algorithms; Distributed rate limiting using Redis/Memcached with Lua scripts to avoid race conditions.
5. **Fault Tolerance & Resilience:** Circuit breakers, exponential backoff with random jitter, bulkheading, idempotency keys for at-least-once message delivery.

---

### 3. Canonical Google-Scale Design Problems to Practice
1. **Design a Distributed Metrics & Alerting System (Google Cloud Monitoring / Datadog):**
   * *Focus:* Ingesting millions of metric data points per second. Row-key design in Bigtable (`[metric_name]#[tenant_id]#[timestamp]`), downsampling via background aggregation jobs, and alerting pipelines.
2. **Design Google Drive / Distributed Cloud Storage:**
   * *Focus:* Chunking large files, block-level deduplication, metadata storage in RDBMS/Bigtable, conflict resolution, synchronization protocol using WebSockets.
3. **Design a Real-Time Proximity Service (Google Maps / Nearby Places):**
   * *Focus:* Spatial indexing (Geohashing vs. Google S2 vs. QuadTrees), read-heavy optimization via distributed caches, static vs. dynamic location updates.
4. **Design YouTube / Video Streaming Platform:**
   * *Focus:* Asynchronous video ingestion pipeline, chunk-based transcoding, CDN caching strategies, metadata retrieval under high read QPS.
5. **Design a Distributed Rate Limiter / API Gateway:**
   * *Focus:* Low-latency token bucket at the edge, synchronization across multi-region datacenters, handling fail-open vs. fail-closed modes.

---

## Part 5: Googleyness & Leadership (G&L)

Google evaluates G&L across **5 core behavioral pillars**. For each pillar, prepare **1–2 concrete STAR stories** from your 5 years of backend engineering experience.

```
       ┌─────────────────────────────────────────────────────────┐
       │             Googleyness & Leadership Pillars            │
       └─────────────────────────────────────────────────────────┘
          │                 │                │                │
          ▼                 ▼                ▼                ▼
   1. Ambiguity &     2. Technical     3. Blameless     4. Mentorship &
      Ownership         Pushback          Outages          Influence
```

### 1. The 5 Core Pillars
1. **Navigating Ambiguity & Taking Initiative:**
   * *Prompt:* Tell me about a time you worked on a project with vague requirements.
   * *Google Rubric:* Did you wait for product managers to give you a spec, or did you interview stakeholders, establish measurable milestones, and write the initial technical design document (RFC)?
2. **Handling Technical Disagreement & Pushback:**
   * *Prompt:* Describe a time you disagreed with a Tech Lead or Product Manager.
   * *Google Rubric:* Did you use data, benchmarks, or prototypes to evaluate the options objectively? Did you commit fully once a team decision was made ("Disagree and Commit")?
3. **Failure, Outages, and Resilience:**
   * *Prompt:* Tell me about your biggest production mistake or technical failure.
   * *Google Rubric:* Did you own the mistake? Did you conduct a blameless post-mortem (RCA)? What architectural safeguards (circuit breakers, automated canary rollouts, alerting) did you institute to ensure this failure class never recurs?
4. **Mentorship & Multiplying Others (Crucial for L5):**
   * *Prompt:* Tell me about a time you elevated a peer or junior engineer.
   * *Google Rubric:* Did you invest time in code reviews, design critiques, or onboardings? Did you help someone overcome a technical roadblock without taking over the work?
5. **Technical Debt vs. Feature Velocity:**
   * *Prompt:* How do you balance delivering business features with refactoring legacy systems?
   * *Google Rubric:* Can you quantify the cost of tech debt (latency, error rates, developer velocity) to business leadership to justify remediation?

---

### 2. The STAR Engineering Matrix (5 YOE Framework)
Write your stories in a concise spreadsheet or document. Allocate your speaking time strictly:
* **Situation (15%):** Context, business impact, and the critical challenge (1–2 sentences).
* **Task (10%):** Specifically what **you** were tasked with (clarify "I" vs. "we").
* **Action (60%):** The technical depth, trade-offs made, team communication, and roadblocks solved.
* **Result (15%):** Quantifiable metrics ($40\%$ latency reduction, \$50k cloud cost saved, zero downtime migration) + your retrospective reflection ("If I were to do this again, I would...").

---

## Part 6: Top Resources & Common Google Pitfalls

### 1. Curated, High-Signal Resources

#### Data Structures & Algorithms
* **LeetCode (Google Tagged, Last 6 Months):** Filter by frequency. Prioritize the patterns outlined above.
* **NeetCode 150:** Excellent structured pattern roadmap for systematic review.
* *Book:* **Elements of Programming Interviews in Python (EPI):** The gold standard for rigor, edge-case coverage, and algorithmic reasoning.

#### System Design
* *Book:* **Designing Data-Intensive Applications (DDIA)** by Martin Kleppmann. (Chapters 5, 6, 7, 8, and 9 are non-negotiable for L5 candidates).
* *Book:* **System Design Interview – An Insider's Guide (Volume 1 & 2)** by Alex Xu.
* *Papers (High Google Signal):*
  * *Bigtable: A Distributed Storage System for Structured Data* (Chang et al.)
  * *Spanner: Google’s Globally-Distributed Database* (Corbett et al.)

#### Mock Interviews
* **Pramp:** Free, peer-to-peer technical and system design practice.
* **Interviewing.io:** Paid, anonymous mocks with verified ex-Google and FAANG Staff engineers. Highly recommended in Weeks 9–11.

---

### 2. The 5 Biggest Pitfalls Causing Hiring Committee Rejections

1. **The "Silent Coder" Syndrome (Failing General Cognitive Ability):**
   * *Failure Mode:* Jumping immediately into code after reading the prompt, staying silent for 10 minutes while thinking.
   * *Why HC Rejects:* Google does not evaluate working code in isolation; they evaluate your **thought process**. If you solve the problem silently, the interviewer has no data points on how you navigate difficulty or evaluate trade-offs.
2. **Sloppy, Script-Like Code Quality:**
   * *Failure Mode:* Writing single-letter variables (`a`, `b`, `res`), massive 60-line monolithic functions, global variables, or ignoring standard language idioms.
   * *Why HC Rejects:* Google evaluates whether your code is "production ready." Code should look like it could pass a strict code review: clean variable names, modularized logic, proper encapsulation.
3. **Hand-Waving Big-O Complexity:**
   * *Failure Mode:* Stating: *"The complexity is probably $O(N)$ because there's one loop,"* ignoring recursive call stack depth, string slicing copies ($O(K)$), or hash collision overheads.
   * *Why HC Rejects:* Google interviewers require exact, formal time and space complexity analysis broken down by parameters (e.g., $O(V + E \log V)$).
4. **Checklist / Buzzword System Design (No Depth):**
   * *Failure Mode:* Drawing a box labeled "Kafka", a box labeled "Redis", and a box labeled "Bigtable" without explaining partition keys, cache invalidation protocols, replication lag, or data durability.
   * *Why HC Rejects:* Interviewers at L5 will drill into your diagram: *"What happens if this broker dies mid-transaction? How do you prevent duplicate processing?"* If you cannot defend the internal mechanics of a component, you will receive a "Lean No Hire" or downlevel to L4.
5. **Defensiveness & Inability to Incorporate Hints:**
   * *Failure Mode:* When the interviewer questions an approach or suggests an edge case, arguing back or doubling down on an unworkable design.
   * *Why HC Rejects:* This directly docks your **Googleyness** score. Google actively tests for coachability and collaborative problem solving. If an interviewer gives you a hint, treat it as a collaborative nudge: *"That's a great point. Let's see how that affects our current boundary conditions."*

---

## Immediate Action Items (Week 1 Kickoff)
1. **IDE Setup:** Set up your Python environment with auto-complete and Copilot disabled. Practice writing code in a basic editor or Google Docs.
2. **Interview Error Log:** Create an error log tracking: `Date | Problem | Pattern | What Tripped Me Up | Optimal Insight`.
3. **Week 1 Problem Target:** Complete 12 problems on Arrays, Two Pointers, and Sliding Window.
