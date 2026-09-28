# Google L4/L5 Coding Question List

**Target:** ~140 problems (not 500). ~100 Medium, ~30 Hard, ~10 Easy warmup.

**Rules:**
- Time every problem (35 min Medium, 45 min Hard).
- If you needed the editorial, it does **not** count until you re-solve it 3–7 days later with no notes.
- Interview in **Python**.
- `[G]` = frequently cited in Google loops. Do these even if you skip neighbors.

Checkboxes are for tracking. Mark `x` only after a **clean timed re-solve**.

---

## How to use this list

1. Follow **weeks 1–8** in order (patterns stack).
2. Weeks 9–12: do **not** add new problems. Re-solve misses + timed mocks from this list.
3. Skip premium only if you must; several Google classics are premium (`261`, `269`, `253`, `340`, `359`, `588`).

**Volume by week:** W1–4 ≈ 80 | W5–8 ≈ 60 | W9–12 = review only.

---

## Week 1 — Arrays, Hashing, Two Pointers, Sliding Window, Intervals

**Milestone:** 18 Mediums cold. Merge Intervals / subarray sum / anagrams without notes.

### Easy (warmup only — 20 min total, not a day)
- [ ] 1. Two Sum `[G]`
- [ ] 217. Contains Duplicate
- [ ] 242. Valid Anagram
- [ ] 283. Move Zeroes

### Medium
- [ ] 49. Group Anagrams `[G]`
- [ ] 238. Product of Array Except Self `[G]`
- [ ] 128. Longest Consecutive Sequence
- [ ] 15. 3Sum `[G]`
- [ ] 11. Container With Most Water `[G]`
- [ ] 167. Two Sum II
- [ ] 75. Sort Colors `[G]`
- [ ] 53. Maximum Subarray `[G]`
- [ ] 560. Subarray Sum Equals K `[G]`
- [ ] 3. Longest Substring Without Repeating Characters `[G]`
- [ ] 424. Longest Repeating Character Replacement
- [ ] 567. Permutation in String
- [ ] 209. Minimum Size Subarray Sum
- [ ] 438. Find All Anagrams in a String `[G]`
- [ ] 56. Merge Intervals `[G]`
- [ ] 57. Insert Interval `[G]`
- [ ] 435. Non-overlapping Intervals
- [ ] 347. Top K Frequent Elements

### Hard
- [ ] 42. Trapping Rain Water `[G]`
- [ ] 76. Minimum Window Substring `[G]`
- [ ] 239. Sliding Window Maximum `[G]`

**Linked list block (do this week or next — Google asks these constantly)**
- [ ] 206. Reverse Linked List
- [ ] 21. Merge Two Sorted Lists
- [ ] 141. Linked List Cycle
- [ ] 19. Remove Nth Node From End of List
- [ ] 143. Reorder List
- [ ] 2. Add Two Numbers `[G]`
- [ ] 138. Copy List with Random Pointer `[G]`
- [ ] 148. Sort List
- [ ] 25. Reverse Nodes in k-Group `[G]` **Hard**

---

## Week 2 — Binary Search (incl. answer-space), Heap, Greedy, Intervals+

**Milestone:** Binary search template from memory (lo/hi, invariant, answer-space).

### Binary search
- [ ] 704. Binary Search
- [ ] 74. Search a 2D Matrix
- [ ] 33. Search in Rotated Sorted Array `[G]`
- [ ] 153. Find Minimum in Rotated Sorted Array
- [ ] 875. Koko Eating Bananas
- [ ] 1011. Capacity To Ship Packages Within D Days
- [ ] 981. Time Based Key-Value Store `[G]`
- [ ] 410. Split Array Largest Sum `[G]` **Hard**
- [ ] 4. Median of Two Sorted Arrays `[G]` **Hard**

### Heap
- [ ] 215. Kth Largest Element in an Array `[G]`
- [ ] 973. K Closest Points to Origin
- [ ] 621. Task Scheduler `[G]`
- [ ] 767. Reorganize String
- [ ] 1834. Single-Threaded CPU
- [ ] 23. Merge k Sorted Lists `[G]` **Hard**
- [ ] 295. Find Median from Data Stream `[G]` **Hard**

### Greedy / intervals
- [ ] 55. Jump Game
- [ ] 45. Jump Game II
- [ ] 134. Gas Station
- [ ] 253. Meeting Rooms II `[G]` (premium; if skip: 2406. Divide Intervals Into Minimum Number of Groups)
- [ ] 452. Minimum Number of Arrows to Burst Balloons

---

## Week 3 — Trees, BST, Recursion, Tries

**Milestone:** LCA, serialize, trie prefix/wildcard. Recursion → iterative if asked.

### Trees / BST
- [ ] 104. Maximum Depth of Binary Tree
- [ ] 226. Invert Binary Tree
- [ ] 100. Same Tree
- [ ] 102. Binary Tree Level Order Traversal `[G]`
- [ ] 103. Binary Tree Zigzag Level Order Traversal `[G]`
- [ ] 199. Binary Tree Right Side View
- [ ] 543. Diameter of Binary Tree
- [ ] 110. Balanced Binary Tree
- [ ] 98. Validate Binary Search Tree `[G]`
- [ ] 230. Kth Smallest Element in a BST
- [ ] 235. Lowest Common Ancestor of a BST
- [ ] 236. Lowest Common Ancestor of a Binary Tree `[G]`
- [ ] 105. Construct Binary Tree from Preorder and Inorder Traversal `[G]`
- [ ] 1448. Count Good Nodes in Binary Tree
- [ ] 863. All Nodes Distance K in Binary Tree `[G]`
- [ ] 124. Binary Tree Maximum Path Sum `[G]` **Hard**
- [ ] 297. Serialize and Deserialize Binary Tree `[G]` **Hard**

### Tries
- [ ] 208. Implement Trie (Prefix Tree) `[G]`
- [ ] 211. Design Add and Search Words Data Structure `[G]`
- [ ] 212. Word Search II `[G]` **Hard**

### Stack / parentheses (pair with trees this week)
- [ ] 20. Valid Parentheses
- [ ] 22. Generate Parentheses `[G]`
- [ ] 150. Evaluate Reverse Polish Notation
- [ ] 71. Simplify Path `[G]`
- [ ] 394. Decode String `[G]`
- [ ] 739. Daily Temperatures
- [ ] 224. Basic Calculator `[G]` **Hard**
- [ ] 227. Basic Calculator II `[G]`

---

## Week 4 — Graphs: BFS/DFS, Topo Sort, Union-Find, Grid

**Milestone:** Course schedule, islands, accounts merge, unweighted shortest path. **2×45 min timed mocks.**

### Grid / BFS / DFS
- [ ] 200. Number of Islands `[G]`
- [ ] 695. Max Area of Island
- [ ] 130. Surrounded Regions
- [ ] 417. Pacific Atlantic Water Flow
- [ ] 994. Rotting Oranges `[G]`
- [ ] 1091. Shortest Path in Binary Matrix
- [ ] 79. Word Search `[G]`
- [ ] 133. Clone Graph `[G]`
- [ ] 542. 01 Matrix

### Topological sort
- [ ] 207. Course Schedule `[G]`
- [ ] 210. Course Schedule II `[G]`
- [ ] 269. Alien Dictionary `[G]` **Hard** (premium; if skip: 953. Verifying an Alien Dictionary + 792-style topo on a DAG you draw)
- [ ] 310. Minimum Height Trees
- [ ] 802. Find Eventual Safe States

### Union-Find
- [ ] 547. Number of Provinces
- [ ] 261. Graph Valid Tree (premium)
- [ ] 323. Number of Connected Components (premium; if skip: 547 is enough + 684)
- [ ] 684. Redundant Connection
- [ ] 721. Accounts Merge `[G]`
- [ ] 1584. Min Cost to Connect All Points

### Hard graph / backtracking
- [ ] 127. Word Ladder `[G]` **Hard**
- [ ] 332. Reconstruct Itinerary
- [ ] 51. N-Queens **Hard**

**Week 4 mock pair (use as full interviews, not practice):**
1. 200 + 207 (or 721)
2. 127 + 56 (or 238)

---

## Week 5 — DP 1: 1D / 2D / knapsack / LIS / string

**Milestone:** 12 DP Medium + 3 Hard. Can explain state, transition, and why it is DP in 60 seconds.

- [ ] 70. Climbing Stairs
- [ ] 198. House Robber
- [ ] 213. House Robber II
- [ ] 322. Coin Change `[G]`
- [ ] 518. Coin Change II
- [ ] 416. Partition Equal Subset Sum
- [ ] 494. Target Sum
- [ ] 62. Unique Paths
- [ ] 64. Minimum Path Sum `[G]`
- [ ] 63. Unique Paths II
- [ ] 152. Maximum Product Subarray
- [ ] 300. Longest Increasing Subsequence `[G]`
- [ ] 1143. Longest Common Subsequence
- [ ] 72. Edit Distance `[G]` **Hard**
- [ ] 91. Decode Ways `[G]`
- [ ] 139. Word Break `[G]`
- [ ] 5. Longest Palindromic Substring `[G]`
- [ ] 647. Palindromic Substrings
- [ ] 309. Best Time to Buy and Sell Stock with Cooldown
- [ ] 221. Maximal Square `[G]`

---

## Week 6 — DP 2: interval, string-hard, tree DP (light)

- [ ] 131. Palindrome Partitioning
- [ ] 97. Interleaving String `[G]`
- [ ] 377. Combination Sum IV
- [ ] 337. House Robber III
- [ ] 140. Word Break II `[G]` **Hard**
- [ ] 10. Regular Expression Matching `[G]` **Hard**
- [ ] 44. Wildcard Matching `[G]` **Hard**
- [ ] 312. Burst Balloons **Hard**
- [ ] 115. Distinct Subsequences **Hard**
- [ ] 123. Best Time to Buy and Sell Stock III **Hard** (optional if 309 is solid)

**Backtracking (do 4 of these if Week 3 stack/parentheses felt weak)**
- [ ] 39. Combination Sum
- [ ] 40. Combination Sum II
- [ ] 46. Permutations
- [ ] 78. Subsets
- [ ] 17. Letter Combinations of a Phone Number `[G]`
- [ ] 37. Sudoku Solver **Hard** (optional)

---

## Week 7 — Graphs hard: Dijkstra, 0-1 BFS, bipartite, weighted / state BFS

**Milestone:** You can set up Dijkstra / 0-1 BFS / multi-state BFS without freezing.

- [ ] 743. Network Delay Time `[G]`
- [ ] 787. Cheapest Flights Within K Stops `[G]`
- [ ] 1631. Path With Minimum Effort
- [ ] 778. Swim in Rising Water `[G]` **Hard**
- [ ] 785. Is Graph Bipartite
- [ ] 399. Evaluate Division `[G]`
- [ ] 329. Longest Increasing Path in a Matrix `[G]` **Hard**
- [ ] 815. Bus Routes `[G]` **Hard**
- [ ] 1293. Shortest Path in a Grid with Obstacles Elimination `[G]` **Hard**
- [ ] 1091. Shortest Path in Binary Matrix (re-solve if Week 4 was slow)
- [ ] 127. Word Ladder (re-solve)

**Stretch (only if the above are clean):**
- [ ] 864. Shortest Path to Get All Keys **Hard**
- [ ] 1192. Critical Connections in a Network **Hard** (Tarjan; skip unless extra time)
- [ ] 126. Word Ladder II **Hard** (skip; implementation tar pit)

---

## Week 8 — Combined patterns + design-flavored coding

**Milestone:** 2 timed coding mocks. These are “Google likes to ask you to implement a type.”

### Design / iterators / rate-limit shaped
- [ ] 146. LRU Cache `[G]`
- [ ] 380. Insert Delete GetRandom O(1) `[G]`
- [ ] 155. Min Stack
- [ ] 173. Binary Search Tree Iterator
- [ ] 341. Flatten Nested List Iterator `[G]`
- [ ] 528. Random Pick with Weight `[G]`
- [ ] 1146. Snapshot Array `[G]`
- [ ] 359. Logger Rate Limiter `[G]` (premium)
- [ ] 362. Design Hit Counter (premium; if skip: 933. Number of Recent Calls + talk through distributed)
- [ ] 460. LFU Cache **Hard** (optional)
- [ ] 588. Design In-Memory File System `[G]` **Hard** (premium; excellent L5 signal)
- [ ] 642. Design Search Autocomplete System `[G]` **Hard** (premium; pairs with Trie)

### Matrix / sweep / “read the problem carefully”
- [ ] 48. Rotate Image `[G]`
- [ ] 54. Spiral Matrix `[G]`
- [ ] 73. Set Matrix Zeroes `[G]`
- [ ] 289. Game of Life `[G]`
- [ ] 31. Next Permutation `[G]`
- [ ] 41. First Missing Positive `[G]` **Hard**
- [ ] 84. Largest Rectangle in Histogram `[G]` **Hard**
- [ ] 68. Text Justification `[G]` **Hard**
- [ ] 843. Guess the Word `[G]` **Hard** (minimax / information; very Google)
- [ ] 340. Longest Substring with At Most K Distinct Characters `[G]` (premium; else 159 if available, or 904. Fruit Into Baskets)

---

## Weeks 9–12 — No new patterns

Re-solve every `[G]` you missed. Use this **mock pool** (45 min, no notes, speak aloud):

### Coding mock sets (pick one set per mock)
| Mock | Problem A | Problem B (if 2-question style) |
|---|---|---|
| A | 76 Minimum Window | 200 Number of Islands |
| B | 127 Word Ladder | 56 Merge Intervals |
| C | 146 LRU Cache | 15 3Sum |
| D | 297 Serialize Tree | 33 Rotated Search |
| E | 42 Trap Rain Water | 207 Course Schedule |
| F | 23 Merge k Lists | 994 Rotting Oranges |
| G | 212 Word Search II | 238 Product Except Self |
| H | 224 Calculator | 721 Accounts Merge |
| I | 329 Longest Increasing Path | 981 Time Map |
| J | 843 Guess the Word | 394 Decode String |
| K | 410 Split Array Largest Sum | 138 Copy Random List |
| L | 1293 Grid Obstacles | 208 Implement Trie |

Do **at least 6** of these timed, talking, with a human or recorder. Weeks 9–11.

---

## Count check

| Bucket | Approx # | Notes |
|---|---|---|
| Easy | ~12 | Warmup only |
| Medium | ~95 | Core |
| Hard | ~30 | Quality; re-solve |
| **Total unique** | **~135–145** | Matches the plan |
| Tagged `[G]` | ~70 | Never skip these |

Premium substitutes are listed inline so you are not blocked.

---

## Python snippets to have in muscle memory

```python
from collections import deque, defaultdict, Counter
import heapq, bisect

# BFS
q = deque([start]); seen = {start}

# Dijkstra
heap = [(0, start)]  # dist, node

# Binary search on answer
lo, hi = 0, max_val
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid): hi = mid
    else: lo = mid + 1

# Union-Find
parent = {}
def find(x):
    parent.setdefault(x, x)
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]
def union(a, b):
    parent[find(a)] = find(b)

# Trie
class Node:
    def __init__(self):
        self.ch = {}
        self.end = False
```

---

## What not to grind

Skip unless a mock exposes a hole:
- Bit-mask DP contest problems
- Max flow / Dinic
- Heavy computational geometry
- Segment trees / Fenwick unless you already know them (not required for L4/L5 SWE)
- 200+ Easy problems
- Random “Google tagged” Easy noise (929 Unique Emails, etc.)
