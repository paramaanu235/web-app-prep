# Amazon DSA question list (curated)

Not 500 problems. Amazon repeats a **narrow band** of patterns plus a few OA-only puzzles. Leadership Principles are in **every** coding round — finish 5 minutes early for LP.

**How this differs from Google**
- More **implementation + hashing + trees + heaps**. Fewer “invent a new graph DP.”
- **OA (online assessment)** is its own genre: logs, “most common word,” two-sum variants, grids.
- Onsite: 1–2 Mediums, or 1 Medium + 1 Hard. Clean code + tests beat a clever incomplete Hard.
- They love **design-flavored coding**: LRU, autocomplete, hit counter, tic-tac-toe.
- Language: Python or Java both fine. Amazon OA often Java/Python/C++.

**Volume:** ~110–130 unique. `[A]` = Amazon-recurring. `[OA]` = online assessment / work-simulation style.

Mark `x` only after a **timed** clean re-solve (35 min Medium, 45 min Hard).

---

## Amazon OA — do these first (2 weeks)

OA is often **2 coding questions**, 70–90 min, no human. Optimize for compiling + passing hidden tests.

### String / hash (OA staples)
- [ ] 937. Reorder Data in Log Files `[A][OA]`
- [ ] 819. Most Common Word `[A][OA]`
- [ ] 387. First Unique Character in a String `[OA]`
- [ ] 242. Valid Anagram
- [ ] 49. Group Anagrams `[A]`
- [ ] 767. Reorganize String `[A]`
- [ ] 791. Custom Sort String
- [ ] 696. Count Binary Substrings `[OA]`
- [ ] 1160. Find Words That Can Be Formed by Characters
- [ ] 819 + follow-up: top K keywords in reviews `[OA]` (see 692)

### Arrays / two pointers / greedy
- [ ] 1. Two Sum `[A]`
- [ ] 15. 3Sum `[A]`
- [ ] 16. 3Sum Closest `[OA]` (movies on a flight / two-sum closest)
- [ ] 167. Two Sum II
- [ ] 11. Container With Most Water
- [ ] 238. Product of Array Except Self `[A]`
- [ ] 53. Maximum Subarray `[A]`
- [ ] 121. Best Time to Buy and Sell Stock `[A]`
- [ ] 122. Best Time to Buy and Sell Stock II
- [ ] 56. Merge Intervals `[A]`
- [ ] 253. Meeting Rooms II `[A]`
- [ ] 435. Non-overlapping Intervals
- [ ] 452. Minimum Number of Arrows to Burst Balloons
- [ ] 763. Partition Labels `[A][OA]`
- [ ] 1710. Maximum Units on a Truck `[A][OA]`
- [ ] 561. Array Partition
- [ ] 189. Rotate Array
- [ ] 41. First Missing Positive **Hard**
- [ ] 42. Trapping Rain Water `[A]` **Hard**

### Sliding window
- [ ] 3. Longest Substring Without Repeating Characters `[A]`
- [ ] 209. Minimum Size Subarray Sum
- [ ] 438. Find All Anagrams in a String
- [ ] 76. Minimum Window Substring `[A]` **Hard**
- [ ] 239. Sliding Window Maximum `[A]` **Hard**
- [ ] 904. Fruit Into Baskets
- [ ] 1004. Max Consecutive Ones III
- [ ] 340. Longest Substring with At Most K Distinct Characters `[A]` (premium; else 159 / 904)

### Heap / top-K / “connect ropes”
- [ ] 215. Kth Largest Element in an Array `[A]`
- [ ] 347. Top K Frequent Elements `[A]`
- [ ] 692. Top K Frequent Words `[A][OA]`
- [ ] 973. K Closest Points to Origin `[A][OA]`
- [ ] 1167. Minimum Cost to Connect Sticks `[A][OA]` (premium; else 1167-style: always merge two smallest)
- [ ] 23. Merge k Sorted Lists `[A]` **Hard**
- [ ] 295. Find Median from Data Stream `[A]` **Hard**
- [ ] 1046. Last Stone Weight
- [ ] 621. Task Scheduler `[A]`
- [ ] 1834. Single-Threaded CPU

### Grid / BFS (OA “zombie / treasure island”)
- [ ] 200. Number of Islands `[A][OA]`
- [ ] 994. Rotting Oranges `[A][OA]` (zombie matrix)
- [ ] 542. 01 Matrix
- [ ] 1091. Shortest Path in Binary Matrix
- [ ] 286. Walls and Gates `[A]` (premium; treasure island)
- [ ] 417. Pacific Atlantic Water Flow `[A]`
- [ ] 695. Max Area of Island
- [ ] 733. Flood Fill
- [ ] 130. Surrounded Regions
- [ ] 490. The Maze (premium)
- [ ] 505. The Maze II (premium)
- [ ] 675. Cut Off Trees for Golf Event `[A]` **Hard**
- [ ] 317. Shortest Distance from All Buildings `[A]` **Hard** (premium)
- [ ] 1293. Shortest Path in a Grid with Obstacles Elimination **Hard**

### Search suggestions / trie OA
- [ ] 1268. Search Suggestions System `[A][OA]`
- [ ] 208. Implement Trie `[A]`
- [ ] 642. Design Search Autocomplete System `[A]` **Hard** (premium)

---

## Onsite coding — by pattern

### Linked list
- [ ] 206. Reverse Linked List `[A]`
- [ ] 21. Merge Two Sorted Lists `[A]`
- [ ] 141. Linked List Cycle
- [ ] 142. Linked List Cycle II
- [ ] 19. Remove Nth Node From End
- [ ] 2. Add Two Numbers `[A]`
- [ ] 445. Add Two Numbers II `[A]`
- [ ] 138. Copy List with Random Pointer `[A]`
- [ ] 143. Reorder List
- [ ] 148. Sort List
- [ ] 25. Reverse Nodes in k-Group `[A]` **Hard**
- [ ] 23. Merge k Sorted Lists (again if OA skipped)
- [ ] 160. Intersection of Two Linked Lists
- [ ] 234. Palindrome Linked List

### Trees / BST (Amazon’s densest onsite cluster)
- [ ] 102. Binary Tree Level Order Traversal `[A]`
- [ ] 103. Binary Tree Zigzag Level Order Traversal `[A]`
- [ ] 107. Binary Tree Level Order Traversal II
- [ ] 199. Binary Tree Right Side View
- [ ] 98. Validate Binary Search Tree `[A]`
- [ ] 235. LCA of BST
- [ ] 236. Lowest Common Ancestor of a Binary Tree `[A]`
- [ ] 230. Kth Smallest Element in a BST `[A]`
- [ ] 173. Binary Search Tree Iterator `[A]`
- [ ] 285. Inorder Successor in BST (premium)
- [ ] 105. Construct Binary Tree from Preorder and Inorder `[A]`
- [ ] 297. Serialize and Deserialize Binary Tree `[A]` **Hard**
- [ ] 124. Binary Tree Maximum Path Sum `[A]` **Hard**
- [ ] 543. Diameter of Binary Tree
- [ ] 112. Path Sum
- [ ] 113. Path Sum II `[A]`
- [ ] 437. Path Sum III
- [ ] 129. Sum Root to Leaf Numbers
- [ ] 314. Binary Tree Vertical Order Traversal `[A]` (premium)
- [ ] 987. Vertical Order Traversal of a Binary Tree **Hard**
- [ ] 545. Boundary of Binary Tree `[A]` (premium)
- [ ] 863. All Nodes Distance K in Binary Tree `[A]`
- [ ] 662. Maximum Width of Binary Tree
- [ ] 958. Check Completeness of a Binary Tree
- [ ] 116. Populating Next Right Pointers in Each Node
- [ ] 117. Populating Next Right Pointers II
- [ ] 226. Invert Binary Tree
- [ ] 101. Symmetric Tree
- [ ] 572. Subtree of Another Tree
- [ ] 110. Balanced Binary Tree
- [ ] 1448. Count Good Nodes in Binary Tree
- [ ] 637. Average of Levels in Binary Tree `[OA]`

### Graphs (beyond grid)
- [ ] 133. Clone Graph `[A]`
- [ ] 207. Course Schedule `[A]`
- [ ] 210. Course Schedule II `[A]`
- [ ] 269. Alien Dictionary `[A]` **Hard** (premium)
- [ ] 261. Graph Valid Tree
- [ ] 323. Number of Connected Components
- [ ] 547. Number of Provinces
- [ ] 721. Accounts Merge `[A]`
- [ ] 399. Evaluate Division
- [ ] 127. Word Ladder `[A]` **Hard**
- [ ] 126. Word Ladder II **Hard** (skip unless extra time)
- [ ] 1192. Critical Connections in a Network `[A]` **Hard** (Tarjan — Amazon classic)
- [ ] 1584. Min Cost to Connect All Points `[A]`
- [ ] 1135. Connecting Cities With Minimum Cost (premium; Kruskal)
- [ ] 787. Cheapest Flights Within K Stops `[A]`
- [ ] 743. Network Delay Time
- [ ] 815. Bus Routes **Hard**
- [ ] 332. Reconstruct Itinerary
- [ ] 785. Is Graph Bipartite
- [ ] 994 / 200 if not done in OA

### Binary search
- [ ] 33. Search in Rotated Sorted Array `[A]`
- [ ] 153. Find Minimum in Rotated Sorted Array
- [ ] 81. Search in Rotated Sorted Array II
- [ ] 34. Find First and Last Position of Element
- [ ] 162. Find Peak Element
- [ ] 875. Koko Eating Bananas
- [ ] 1011. Capacity To Ship Packages Within D Days `[A]`
- [ ] 410. Split Array Largest Sum **Hard**
- [ ] 4. Median of Two Sorted Arrays `[A]` **Hard**
- [ ] 981. Time Based Key-Value Store `[A]`
- [ ] 528. Random Pick with Weight `[A]`
- [ ] 702. Search in a Sorted Array of Unknown Size (premium)

### Stack / parse / monotonic
- [ ] 20. Valid Parentheses `[A]`
- [ ] 22. Generate Parentheses `[A]`
- [ ] 32. Longest Valid Parentheses **Hard**
- [ ] 150. Evaluate Reverse Polish Notation `[A]`
- [ ] 224. Basic Calculator `[A]` **Hard**
- [ ] 227. Basic Calculator II `[A]`
- [ ] 394. Decode String `[A]`
- [ ] 71. Simplify Path `[A]`
- [ ] 739. Daily Temperatures `[A]`
- [ ] 496. Next Greater Element I
- [ ] 503. Next Greater Element II
- [ ] 84. Largest Rectangle in Histogram `[A]` **Hard**
- [ ] 85. Maximal Rectangle **Hard**
- [ ] 735. Asteroid Collision `[A]`
- [ ] 402. Remove K Digits
- [ ] 316. Remove Duplicate Letters
- [ ] 155. Min Stack `[A]`
- [ ] 636. Exclusive Time of Functions `[A]`
- [ ] 901. Online Stock Span

### Backtracking
- [ ] 17. Letter Combinations of a Phone Number `[A]`
- [ ] 39. Combination Sum
- [ ] 40. Combination Sum II
- [ ] 46. Permutations
- [ ] 47. Permutations II
- [ ] 78. Subsets
- [ ] 79. Word Search `[A]`
- [ ] 212. Word Search II `[A]` **Hard**
- [ ] 51. N-Queens **Hard**
- [ ] 37. Sudoku Solver **Hard** (optional)
- [ ] 22. Generate Parentheses (again)

### DP (Amazon asks fewer than Google, but not zero)
- [ ] 70. Climbing Stairs
- [ ] 198. House Robber `[A]`
- [ ] 213. House Robber II
- [ ] 322. Coin Change `[A]`
- [ ] 518. Coin Change II
- [ ] 300. Longest Increasing Subsequence `[A]`
- [ ] 139. Word Break `[A]`
- [ ] 140. Word Break II `[A]` **Hard**
- [ ] 91. Decode Ways `[A]`
- [ ] 62. Unique Paths
- [ ] 64. Minimum Path Sum
- [ ] 221. Maximal Square `[A]`
- [ ] 5. Longest Palindromic Substring `[A]`
- [ ] 72. Edit Distance **Hard**
- [ ] 1143. Longest Common Subsequence
- [ ] 152. Maximum Product Subarray `[A]`
- [ ] 416. Partition Equal Subset Sum
- [ ] 377. Combination Sum IV
- [ ] 1235. Maximum Profit in Job Scheduling `[A]` **Hard**
- [ ] 472. Concatenated Words `[A]` **Hard**
- [ ] 1326. Minimum Number of Taps to Open to Water a Garden / 45. Jump Game II
- [ ] 55. Jump Game `[A]`
- [ ] 45. Jump Game II
- [ ] 134. Gas Station `[A]`
- [ ] 10. Regular Expression Matching **Hard** (stretch)

### Design-as-code (Amazon onsite loves these)
- [ ] 146. LRU Cache `[A]` **must type from memory**
- [ ] 460. LFU Cache `[A]` **Hard**
- [ ] 380. Insert Delete GetRandom O(1) `[A]`
- [ ] 381. Insert Delete GetRandom O(1) — Duplicates **Hard**
- [ ] 359. Logger Rate Limiter `[A]`
- [ ] 362. Design Hit Counter `[A]`
- [ ] 346. Moving Average from Data Stream `[A]`
- [ ] 1429. First Unique Number (premium)
- [ ] 348. Design Tic-Tac-Toe `[A]`
- [ ] 353. Design Snake Game
- [ ] 588. Design In-Memory File System `[A]` **Hard**
- [ ] 1396. Design Underground System
- [ ] 1472. Design Browser History
- [ ] 1656. Design an Ordered Stream
- [ ] 1146. Snapshot Array `[A]`
- [ ] 716. Max Stack (premium)
- [ ] 895. Maximum Frequency Stack **Hard**
- [ ] 432. All O`one Data Structure **Hard** (stretch)
- [ ] 341. Flatten Nested List Iterator `[A]`
- [ ] 251. Flatten 2D Vector (premium)
- [ ] 284. Peeking Iterator
- [ ] 232. Implement Queue using Stacks
- [ ] 225. Implement Stack using Queues
- [ ] 355. Design Twitter (optional)

### Matrix / “read carefully”
- [ ] 48. Rotate Image `[A]`
- [ ] 54. Spiral Matrix `[A]`
- [ ] 59. Spiral Matrix II
- [ ] 73. Set Matrix Zeroes `[A]`
- [ ] 36. Valid Sudoku
- [ ] 74. Search a 2D Matrix
- [ ] 240. Search a 2D Matrix II `[A]`
- [ ] 289. Game of Life
- [ ] 31. Next Permutation `[A]`
- [ ] 68. Text Justification **Hard** (less Amazon than Google; still useful)

---

## High-signal Amazon uniques (don’t skip)

These show up in “recent Amazon” reports more than generic NeetCode:

| # | Problem | Why |
|---|---|---|
| 937 | Reorder Data in Log Files | OA almost guaranteed historically |
| 819 | Most Common Word | OA |
| 1268 | Search Suggestions System | OA + trie |
| 1192 | Critical Connections | Tarjan bridges — SDE2 tell |
| 1167 | Min Cost to Connect Sticks | Huffman / heap |
| 763 | Partition Labels | greedy + last index |
| 545 | Boundary of Binary Tree | messy tree impl |
| 314 | Vertical Order (not 987) | BFS + col index |
| 636 | Exclusive Time of Functions | stack of functions |
| 348 | Tic-Tac-Toe | O(1) move |
| 146 | LRU | every level |
| 200 + 994 | Islands / rotting | grid BFS |
| 138 | Copy Random List | graph-on-list |
| 297 | Serialize tree | |
| 253 | Meeting Rooms II | heap |
| 973 | K Closest | heap / quickselect |
| 692 | Top K Words | heap + tie-break |
| 675 | Cut Off Trees | multi BFS |
| 472 | Concatenated Words | word break on a set |
| 1235 | Job Scheduling | DP + bisect |
| 445 | Add Two Numbers II | stack, no reverse list follow-up |

---

## Target counts

| | Count | Notes |
|---|---|---|
| OA cluster | **25–30** | Do before applying |
| Medium | **80–95** | Core |
| Hard | **20–28** | LRU internals, islands-hard, Tarjan, serialize, trap rain, merge k |
| Easy | **10** | Warmup only |
| **Total unique** | **~120** | Overlap with the Google list is large — don’t double-grind |

If you already finished the Google list: add **OA strings**, **Critical Connections**, **Search Suggestions**, **Connect Sticks**, **Partition Labels**, **Vertical Order 314**, **Exclusive Time**, **Tic-Tac-Toe**, **Add Two Numbers II**, **Concatenated Words**. That delta is the Amazon-specific work.

---

## Live-interview framework (Amazon flavor)

1. Clarify (duplicates, sorted, in-place, n=10^5, follow-up constraints).
2. Example + 1 edge.
3. Brute → complexity → better. Name the pattern.
4. Code in the language you’ll use in OA (same as onsite).
5. Walk an example. Null, empty, 1 element, overflow, disconnected.
6. **Stop with 5 min left.** “Tradeoff if this is a stream / concurrent map?”
7. LP probe: “Tell me about a time you disagreed…” — have 2 stories ready **in the same interview**.

Amazon rejects **working code with silent arrogance** and **almost-correct code with no tests** equally.

---

## Mock sets (45 min, talk aloud)

| Mock | A | B (if two-question) |
|---|---|---|
| OA-1 | 937 Log Files | 973 K Closest |
| OA-2 | 819 Most Common Word | 200 Islands |
| OA-3 | 1268 Search Suggestions | 763 Partition Labels |
| OA-4 | 994 Rotting Oranges | 1 Two Sum unique pairs |
| Onsite-1 | 146 LRU | 56 Merge Intervals |
| Onsite-2 | 297 Serialize | 215 Kth Largest |
| Onsite-3 | 236 LCA | 3 Longest Substring |
| Onsite-4 | 138 Copy Random | 33 Rotated Search |
| Onsite-5 | 1192 Critical Connections | 20 Valid Parentheses |
| Onsite-6 | 23 Merge k | 102 Level Order |
| Onsite-7 | 239 Sliding Window Max | 98 Validate BST |
| Onsite-8 | 348 Tic-Tac-Toe | 394 Decode String |
| Onsite-9 | 721 Accounts Merge | 42 Trap Rain |
| Onsite-10 | 127 Word Ladder | 155 Min Stack |

Do **OA-1..4 timed without notes** before you submit the application.

---

## What Amazon does **not** need

- Segment trees / Fenwick (unless you already know them)
- Max flow
- Heavy geometry
- Bitmask DP contests
- 200 Easy
- System-design-as-code beyond LRU/LFU/autocomplete/file system

---

## SDE level calibration (coding only)

| Level | Coding bar |
|---|---|
| SDE 1 | Clean Medium in 25–30 min; OA strong; trees + hash + BFS |
| SDE 2 (L5-ish) | Medium without hints; one Hard (LRU, serialize, trap, merge k, Tarjan); talk tradeoffs |
| SDE 3 | Same plus follow-ups (stream, concurrent, scale the data structure); you lead |

Leadership Principles are scored **in the coding round**, not only in the “bar raiser.” Bias for Action = you pick an approach and code. Dive Deep = you test. Have Backbone = you defend complexity. Earn Trust = you don’t hide a bug.

---

## Python OA kit (if you interview in Python)

```python
from collections import deque, defaultdict, Counter, OrderedDict
import heapq, bisect
# LRU: OrderedDict move_to_end / popitem(last=False)
# logs: digit vs letter — `s.split()[1][0].isdigit()`
```

Java: `ArrayDeque`, `PriorityQueue`, `LinkedHashMap(accessOrder=true)` for LRU — see `java_interview_cheatsheet.md`.
