# Python Interview Muscle Memory

Practise these from a blank editor, explain the invariant, and adapt them to the input contract. Short comments explaining state or an invariant are useful; avoid narrating every assignment.

**Usage:** Python 3.8+ baseline unless a feature is explicitly version-marked. Import the kit below when extracting functions. API demonstrations use contextual variables; complete functions state their contracts. These are preparation notes, not a prediction of interview questions. During the interview, follow the permitted-resource rules.

**Validation, 7 September 2026:** All 41 Python code fences compile on Python 3.12.14. Selected extracted functions passed 22,463 behavioral checks, including brute-force/randomized comparisons, earlier failure cases, 5,000-node tree codecs, and 10,000 dynamic union operations. Compilation of API fragments does not supply their contextual variables; tests are not an exhaustive proof for every input.

---

## 0. Import kit (first 15 seconds)

```python
from collections import deque, defaultdict, Counter, OrderedDict
from functools import lru_cache
from typing import List, Optional, Dict, Set, Tuple
import heapq, bisect, math, itertools, sys

# sys.getrecursionlimit()  # inspect; prefer iterative traversal for long chains
```

**Explanation:** `deque` = BFS / sliding window. `defaultdict` = graphs and grouping without `if key in`. `Counter` = frequencies / anagrams. `heapq` = top-k, Dijkstra, merge-k. `bisect` = binary search on a sorted list. `lru_cache(None)` = memoized DP. `math.inf` avoids choosing an insufficient finite sentinel for “unreachable.” Typing imports are optional; use the provided signature where applicable.

Do **not** auto-raise the recursion limit. Inspect it with `sys.getrecursionlimit()`; it is commonly 1,000 in CPython but is configurable. For a chain of 10^5 nodes, use an explicit stack. The usable depth is platform-dependent, and an excessively high limit can crash the process. [Python recursion-limit documentation](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit)

---

## 1. Node skeletons (write immediately when they say “linked list / tree”)

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Node:  # graph / N-ary
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
```

**Explanation:** LeetCode usually provides these. In a Google doc/interview you often must write them. Use `next=None` / `left=None` so you can construct `ListNode(1)` without extra args.

**Critical:** `neighbors=None` then `neighbors if neighbors is not None else []` — never `neighbors=[]`. A mutable default is shared across all instances; every graph node would share one list.

`Node` is for clone-graph / N-ary trees. Don’t mix `TreeNode.left/right` with adjacency lists.

---

## 2. Collections — use these, don’t roll your own

```python
# deque: O(1) both ends. NEVER pop(0) on a list.
q = deque([start])
q.append(x)       # right
q.appendleft(x)   # left
q.pop()           # right
q.popleft()       # left  ← BFS
q[0]; q[-1]       # peek

# defaultdict: missing key → factory
g = defaultdict(list)     # graph
cnt = defaultdict(int)    # frequencies
dist = defaultdict(lambda: math.inf)

# Counter
c = Counter(s)            # str/list → freq
c.most_common(k)          # [(item, count), ...]
c.keys() & d.keys()       # intersection of keys
Counter(a) == Counter(b)  # anagram
c + d; c - d              # add / subtract counts (no negatives on -)

# set
seen = set()
seen.add(x); seen.discard(x)   # discard does not throw
a | b; a & b; a - b; a ^ b

# dict
d.get(k, default)
d.setdefault(k, []).append(x)
d.pop(k, None)
for k, v in d.items():
    ...
# Python 3.7+ dicts are insertion-ordered (LRU, first unique)
```

**Explanation:**

- **`deque`:** `list.pop(0)` / `list.insert(0, x)` are O(n). Interviewers notice. BFS must `popleft`. Monotonic queue for sliding-window max also uses `deque`. Indexing `q[0]` / `q[-1]` is O(1); arbitrary index is O(n) — don’t treat it like a random-access array.
- **`defaultdict(list)`:** `g[u].append(v)` never throws. Factory runs **per missing key**, so each key gets its own new list. `defaultdict(lambda: math.inf)` is for distances when nodes are not `0..n-1`.
- **`Counter`:** Built from any iterable. For N input items and U distinct keys, frequency construction plus a small top-k selection is expected O(N + U log(k+1)); requesting all entries can use sorting. Do not assume every `most_common` call uses the same implementation path. `c - d` **drops** counts ≤ 0; retain signed counts explicitly when needed. Comparing Counters freshly built from two strings is an anagram test. Zero-count equality semantics changed in Python 3.10, so avoid depending on them across runtimes.
- **`set`:** `discard` vs `remove`: `remove` raises `KeyError` if absent. Use `discard` unless you want the exception. `| & - ^` are set algebra; result is a new set.
- **`dict`:** `d[k]` throws; `d.get(k, default)` does not. `setdefault(k, []).append(x)` is the one-liner graph build if you don’t use defaultdict. **Insertion order is guaranteed** (3.7+): first-unique-character, LRU via `OrderedDict` / move-to-end, reconstructing grouped items in input order.

---

## 3. Sorting / key functions

```python
a.sort()                         # in-place
b = sorted(a, reverse=True)
pairs.sort(key=lambda x: x[1])   # by second field
pairs.sort(key=lambda x: (-x[1], x[0]))  # count desc, then name asc
intervals.sort()                 # sorts by first element, then second
s = ''.join(sorted(s))           # anagram key
words.sort(key=len)

# decorate-sort-undecorate when key is expensive
# stable sort: equal keys keep original order — use it
```

**Explanation:** `list.sort()` mutates and returns `None` — never write `a = a.sort()`. `sorted(a)` returns a new list.

`key=` runs once per element (Schwartzian), then compares those keys. Tuple keys compare left-to-right. Negate a number for descending on that field: `(-count, name)` → high count first, then name ascending. You **cannot** negate a string; for string desc use `reverse=True` or a second pass.

`intervals.sort()` on `[start, end]` sorts by start, then end — that is exactly what merge-intervals needs.

Timsort is **stable**: equal keys keep original order. Two-pass sorts work: sort by secondary key first, then by primary.

Anagram grouping key: `''.join(sorted(s))` is O(k log k) per string. For lowercase-only, a 26-count tuple is O(k) and also hashable.

---

## 4. Heap (`heapq`; portable max-heap via negation)

```python
h = []
heapq.heappush(h, x)
x = heapq.heappop(h)
x = h[0]                         # peek min
heapq.heapify(a)                 # in-place O(n)

# max-heap: negate
heapq.heappush(h, -x)
x = -heapq.heappop(h)

# k largest / smallest
heapq.nlargest(k, a)
heapq.nsmallest(k, a)

# tuples: ordered by first element, then second
heapq.heappush(h, (dist, node))
heapq.heappush(h, (freq, idx, val))  # idx breaks ties when val is incomparable

# max-heap of tuples
heapq.heappush(h, (-priority, node))

# “remove” from heap: lazy delete
# push new state; skip popped entries that are stale vs a dist[] / valid map
```

**Explanation:** Negation works on older runtimes. Python 3.14 added public `heapify_max`, `heappush_max`, and `heappop_max`; use them only when supported. For arbitrary objects, use a unique tie-breaker: `(-priority, next(counter), obj)`, with `counter = itertools.count()`. [Python heap documentation](https://docs.python.org/3/library/heapq.html)

**Tuple comparison:** Equal priorities cause comparison of the next field. Custom nodes generally have no ordering; numeric lists do compare lexicographically, but arbitrary payloads may not. A unique counter prevents payload comparison and makes equal-priority handling deterministic.

`h[0]` peeks without popping. `heapify` is O(n), cheaper than n pushes (O(n log n)).

**No decrease-key.** Dijkstra / “update a node’s distance” = push a new `(new_dist, node)` and **ignore stale pops** where `d != dist[u]`. Same pattern for lazy-delete in running medians / invalid tasks.

For a small k, `nlargest(k, a)` uses a bounded selection with O(n log(k+1)) time; k=1 can use a linear scan and selecting all can use sorting. Heap iteration itself is not sorted.

```python
def kth_largest(nums, k):
    # nums is a sequence; 1 <= k <= len(nums). Duplicates count separately.
    if not 1 <= k <= len(nums):
        raise ValueError("invalid k")
    heap = []
    for value in nums:
        if len(heap) < k:
            heapq.heappush(heap, value)
        else:
            heapq.heappushpop(heap, value)
    return heap[0]
```

O(n log(k+1)) time, O(k) space. `heappushpop` removes the smaller of the candidate and old minimum; `heapreplace` always removes the old minimum and requires a nonempty heap. They are not interchangeable without checking the candidate.

---

## 5. Binary search

### `bisect` (on a **sorted** array)

```python
i = bisect.bisect_left(a, x)   # first index with a[i] >= x
i = bisect.bisect_right(a, x)  # first index with a[i] > x
# count of x:
bisect.bisect_right(a, x) - bisect.bisect_left(a, x)
# insert keeping sorted:
bisect.insort(a, x)            # O(n) insert; judge total number of operations
```

**Explanation:** Array **must already be sorted** or results are garbage. `bisect_left` = insertion point before existing `x`s (lower_bound). `bisect_right` = after existing `x`s (upper_bound).

- First index ≥ x: `bisect_left`
- First index > x: `bisect_right`
- Last index ≤ x: `bisect_right(a, x) - 1` (check ≥ 0)
- Count of x: right − left

`insort` shifts elements O(n). Use only when n is small or you need a short sorted list (LIS tails is `bisect` without `insort` of a huge array).

### Manual — find exact / leftmost / rightmost

```python
def binary_search(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def leftmost(a, target):          # first >= target (lower_bound)
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo                     # lo == len(a) → all smaller

def rightmost(a, target):         # last <= target
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1
```

**Explanation:** Two loop styles:

1. `lo, hi = 0, n-1` and `while lo <= hi` with `hi = mid-1` / `lo = mid+1`. Classic exact match. `mid` is always a valid index.
2. `lo, hi = 0, n` and `while lo < hi` with `hi = mid` (not mid-1). The unresolved element interval is `[lo, hi)`, but the insertion boundary lies in **`[lo, hi]`** and may equal n. For lower bound, all indices below lo have values `< target`; all indices at or above hi have values `>= target`.

Say the invariant out loud. On termination, `lo == hi` is the insertion boundary. Dry-run an empty input, n=1, duplicates, and “all elements < target.”

`rightmost` returns `-1` if every element is > target. Check that before indexing.

### Binary search on the **answer** (Koko, split array, capacity)

```python
def first_feasible(lo, hi, feasible):
    # Integer bounds lo <= hi; false then true; feasible(hi) must be true.
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def last_feasible(lo, hi, feasible):
    # Integer bounds lo <= hi; true then false; feasible(lo) must be true.
    while lo < hi:
        mid = (lo + hi + 1) // 2  # upper midpoint ensures progress
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

**Explanation:** You are not searching an array. You are searching a **monotonic predicate** `feasible(x)`.

- Minimize x such that `feasible(x)` is true (speed, capacity, max-subarray-sum): if mid works, try smaller → `hi = mid`. If not, need larger → `lo = mid + 1`.
- Maximize x: if mid works, try larger. **`mid = (lo + hi) // 2` rounds down**, so `lo = mid` never moves when `hi = lo+1`. Fix: `mid = (lo + hi + 1) // 2` (round up).

If one feasibility check costs C, the search costs O(C log(RANGE+1)). Verify monotonicity and the feasible endpoint; these templates do not themselves detect an entirely infeasible range.

---

## 6. Sliding window

```python
def longest_at_most_k_distinct(s, k):
    if k <= 0:
        return 0
    counts = Counter()
    left = best = 0
    for right, ch in enumerate(s):
        counts[ch] += 1
        while len(counts) > k:
            old = s[left]
            counts[old] -= 1
            if counts[old] == 0:
                del counts[old]
            left += 1
        best = max(best, right - left + 1)
    return best

def min_window(s, t):
    # Return the shortest substring covering t's multiplicities, or "".
    if not t:
        return ""
    need, window = Counter(t), Counter()
    need_met = left = 0
    best_length, best_start = math.inf, 0
    for right, ch in enumerate(s):
        if ch in need:
            window[ch] += 1
            if window[ch] == need[ch]:
                need_met += 1
        while need_met == len(need):
            if right - left + 1 < best_length:
                best_length, best_start = right - left + 1, left
            old = s[left]
            if old in need:
                window[old] -= 1
                if window[old] < need[old]:
                    need_met -= 1
            left += 1
    return "" if best_length == math.inf else s[best_start:best_start + best_length]

def max_window_sum(nums, k):
    # Nonempty fixed-size windows; handles negative numbers.
    if not 1 <= k <= len(nums):
        raise ValueError("invalid window size")
    total = sum(nums[i] for i in range(k))
    best = total
    for right in range(k, len(nums)):
        total += nums[right] - nums[right - k]
        best = max(best, total)
    return best

def sliding_window_max(nums, k):
    if not 1 <= k <= len(nums):
        raise ValueError("invalid window size")
    queue, result = deque(), []  # indices with decreasing values
    for i, value in enumerate(nums):
        while queue and queue[0] <= i - k:
            queue.popleft()
        while queue and nums[queue[-1]] <= value:
            queue.pop()
        queue.append(i)
        if i >= k - 1:
            result.append(nums[queue[0]])
    return result
```

**Explanation:** One `right` pointer expands; `left` only moves forward. Each index enters and leaves at most once → O(n).

**Longest valid:** expand always; shrink until valid; then record length. Example: longest substring with ≤ k distinct (`len(cnt) > k`).

**Shortest valid (LC 76):** expand until the constraint is met; then shrink **while still valid** and record. `need_met` counts how many **unique required chars** are fully satisfied — O(1) validity, not O(|alphabet|) per step.

For distinct counts, **remove zero-count keys** so `len(counts)` reflects the active window. A Counter retains zero entries unless removed.

Complexities: distinct window expected O(n) time and O(min(alphabet, k+1)) space; minimum window expected O(len(s)+len(t)) time and O(distinct(t)) auxiliary space, excluding returned text. Fixed sum is O(n)/O(1). Sliding maximum is O(n)/O(k), excluding output: each index is pushed and removed at most once.

Do not apply a sum-based shrinking window blindly when negative numbers are allowed; the required monotonicity may fail. Use prefix sums when appropriate.

---

## 7. Two pointers / intervals

```python
def two_sum_sorted(nums, target):
    # Ascending input; return zero-based indices or None.
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        total = nums[lo] + nums[hi]
        if total == target:
            return lo, hi
        if total < target:
            lo += 1
        else:
            hi -= 1
    return None

# merge intervals (sort first)
intervals.sort()
merged = []
for s, e in intervals:
    if not merged or s > merged[-1][1]:
        merged.append([s, e])
    else:
        merged[-1][1] = max(merged[-1][1], e)

# sweep line
events = []
for s, e in intervals:
    events.append((s, +1))
    events.append((e, -1))       # half-open [s,e), assumes s < e
events.sort()                   # -1 before +1: reuse a room at the same time
active = peak = 0
for time, delta in events:
    active += delta
    peak = max(peak, active)
# Closed intervals need starts before ends at ties: key=lambda event: (event[0], -event[1]).
```

**Explanation:**

- **Two-sum on sorted array:** when the sum is too small, discard the left index; when too big, discard the right. O(n) time/O(1) auxiliary space. For 3Sum, sort, skip repeated fixed values with `if i > 0 and nums[i] == nums[i-1]: continue`, and skip duplicate left/right values after each match.
- **Merge:** after sort by start, the only interval that can overlap the current one is `merged[-1]`. If next start is `>` last end, no overlap (touching: `s == last_end` — ask if touching merges; usually `s <= last_end` merges).
- **Sweep:** convert intervals to events. Running `active` count = how many intervals cover this time. Meeting rooms = max `active`. **Tie-break:** if a meeting ends at T and another starts at T, process `-1` before `+1` so you reuse the room. Sort key `(time, type)` with end type < start type.

---

## 8. Prefix sums / difference array

```python
pref = [0]
for x in a:
    pref.append(pref[-1] + x)
# sum[i..j] inclusive:
pref[j + 1] - pref[i]

# 2D prefix
# P[i+1][j+1] = P[i][j+1] + P[i+1][j] - P[i][j] + A[i][j]
# rect (r1,c1)–(r2,c2) inclusive:
# P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]

# difference array: range increment
diff = [0] * (n + 1)
diff[l] += val
diff[r + 1] -= val
cur = 0
for i in range(n):
    cur += diff[i]
    a[i] += cur
```

**Explanation:** Prefix turns range-sum into O(1) after O(n) build. `pref[0] = 0` so `sum[0..j] = pref[j+1]`. Off-by-one: `pref` has length `n+1`.

Subarray-sum-equals-K: as you walk, `need = pref - k`; if `need` was seen as a previous prefix, a subarray ends here. Store prefix **counts** in a dict (`Counter`), not just existence, if you need number of subarrays.

```python
def subarray_sum_count(nums, target):
    frequencies = {0: 1}  # empty prefix allows subarrays starting at index 0
    prefix = result = 0
    for value in nums:
        prefix += value
        result += frequencies.get(prefix - target, 0)  # query before insertion
        frequencies[prefix] = frequencies.get(prefix, 0) + 1
    return result
```

Expected O(n) time and O(n) space. Supports zeros and negative numbers; repeated prefix sums represent distinct starting positions.

**2D:** inclusion-exclusion. The `+ P[r1][c1]` adds back the double-subtracted corner. Build with +1 index padding so you never special-case row 0.

**Difference array:** inverse of prefix. “Add `val` to range `[l, r]`” is O(1) writes. After all updates, one prefix pass materializes the array. Use when you have many range updates, few queries (or one final array). Corporate-flight-bookings, range-addition problems.

---

## 9. Monotonic stack

```python
def next_greater_indices(nums):
    result, stack = [-1] * len(nums), []
    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] < value:
            result[stack.pop()] = i
        stack.append(i)
    return result  # -1 if no strictly greater element to the right

def previous_greater_indices(nums):
    result, stack = [-1] * len(nums), []
    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] <= value:
            stack.pop()
        if stack:
            result[i] = stack[-1]
        stack.append(i)
    return result
```

**Explanation:** The next-greater stack holds unresolved indices in **non-increasing value order from bottom to top**. Equal values remain because the comparison is strict. Each index is pushed/popped at most once: O(n) time and O(n) auxiliary space.

Store **indices**, not values: you need positions for width (histogram, trapping rain).

- Next greater: resolve pending indices while their values are `< x` (`<=` for greater-or-equal).
- Next smaller: reverse the comparison to `> x`.
- Previous strictly greater: first pop values `<= x`, then record the surviving top before pushing the new index. Equal values must not qualify.

**Histogram (LC 84):** for each bar, width = (next smaller index − previous smaller index − 1) × height. Sentinels of height 0 at both ends flush the stack.

**Trapping rain (LC 42)** can be monotonic stack **or** two-pointer; two-pointer is shorter in interview.

---

## 10. Linked list

```python
# dummy head — useful when removal/merge might change the head
dummy = ListNode(0, head)
prev = dummy

# reverse
def reverse(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev

# reverse k nodes starting at head (k >= 1; assume k nodes exist)
def reverse_k(head, k):
    prev, cur = None, head
    for _ in range(k):
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    return prev, cur             # new head, node after block

# slow/fast
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# even: slow is second middle; for first middle, prev-of-slow

# cycle (Floyd)
# intersection: len trick or set of ids
```

**Explanation:** Dummy node so you never special-case “head is removed / list becomes empty.” Return `dummy.next`.

**Reverse:** three pointers. Save `nxt` **before** rewiring or you lose the rest of the list. New head is `prev`.

**Reverse-k:** same loop, k times. After reverse, original `head` is the tail of the block; `cur` is the first node of the remainder. Caller stitches `prev_tail.next = new_head` and `old_head.next = next_block`.

**Slow/fast:** `fast` moves 2, `slow` moves 1. When `fast` hits end, `slow` is mid. Even length: this lands on the **second** middle. Cycle detect: if they meet, there is a cycle. Cycle start: reset one pointer to head, both step 1; meeting point is start (Floyd).

**Intersection:** two pointers swap lists when they hit `None`; they meet at intersection or both `None`. Don’t compare `val` — compare **object identity** (`is`).

```python
def has_cycle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False

def merge_lists(a, b):
    # Ascending, acyclic, disjoint lists; reuses and mutates their nodes.
    dummy = tail = ListNode()
    while a is not None and b is not None:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next

def intersection(a, b):
    # Both lists must be acyclic. Values need not be unique.
    left, right = a, b
    while left is not right:
        left = left.next if left is not None else b
        right = right.next if right is not None else a
    return left
```

Cycle detection is O(n) time/O(1) space. Merge and intersection are O(m+n) time/O(1) auxiliary space. Use a dummy where it simplifies head changes; full-list reversal does not require one.

---

## 11. Trees

```python
# DFS recursive
def tree_dfs(node):
    if not node:
        return
    tree_dfs(node.left)
    tree_dfs(node.right)

# iterative preorder
st = [root]
while st:
    node = st.pop()
    if not node:
        continue
    st.append(node.right)
    st.append(node.left)

# inorder iterative
st, cur, out = [], root, []
while st or cur:
    while cur:
        st.append(cur)
        cur = cur.left
    cur = st.pop()
    out.append(cur.val)
    cur = cur.right

def level_order(root):
    if root is None:
        return []
    result, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left is not None: q.append(node.left)
            if node.right is not None: q.append(node.right)
        result.append(level)
    return result

# LCA binary tree
def lca(root, p, q):
    # Both target node references must exist in this binary tree.
    if not root or root is p or root is q:
        return root
    L = lca(root.left, p, q)
    R = lca(root.right, p, q)
    if L and R:
        return root
    return L or R

# Integer node values; iterative preorder with null sentinels.
def serialize(root):
    tokens, stack = [], [root]
    while stack:
        node = stack.pop()
        if node is None:
            tokens.append("#")
        else:
            tokens.append(str(node.val))
            stack.append(node.right)
            stack.append(node.left)
    return ",".join(tokens)

def deserialize(data):
    # Requires valid output of serialize, including "#" for the empty tree.
    tokens = iter(data.split(","))
    first = next(tokens)
    if first == "#":
        return None
    root = TreeNode(int(first))
    stack = [(root, 0)]  # next child: 0 = left, 1 = right
    for token in tokens:
        parent, side = stack[-1]
        child = None if token == "#" else TreeNode(int(token))
        if side == 0:
            parent.left = child
            stack[-1] = (parent, 1)
        else:
            parent.right = child
            stack.pop()
        if child is not None:
            stack.append((child, 0))
    return root

def valid_bst(root, low=-math.inf, high=math.inf):
    # Strict BST: no duplicate values; recursive depth is tree height.
    if root is None:
        return True
    return (low < root.val < high
            and valid_bst(root.left, low, root.val)
            and valid_bst(root.right, root.val, high))

def height_or_unbalanced(root):
    if root is None:
        return 0
    left = height_or_unbalanced(root.left)
    if left == -1:
        return -1
    right = height_or_unbalanced(root.right)
    if right == -1 or abs(left - right) > 1:
        return -1
    return 1 + max(left, right)
```

**Explanation:**

- **Null check first.** Dereferencing a missing node raises `AttributeError`; recursion depth is a separate concern.
- **Iterative preorder:** stack is LIFO, so push **right then left** to visit left first.
- **Iterative inorder:** walk left spine, pop = visit, then go right. This is also BST iterator (`hasNext`/`next`).
- **Level BFS:** `for _ in range(len(q))` freezes the current level size. Don’t use `while q` without that if you need per-level lists (zigzag, right-side view).
- **LCA:** if `p` and `q` are in different subtrees, both `L` and `R` are non-null → `root` is LCA. If both in one side, that side’s result bubbles up. Uses `is` (same node object), not `val` (values may duplicate unless the problem says BST unique).
- **Serialize:** `#` marks null so preorder is reconstructible. Both supplied codecs use explicit stacks and handle deep chains. Avoid concatenating recursively returned lists, which costs Θ(n²) copying on a skewed tree. Deque token consumption would use `popleft()`, never `pop(0)`.

BST extras: inorder is sorted. Validate BST must thread `low < node.val < high`, not just “left < me < right” (fails on `[5,1,4,null,null,3,6]`).

Complexities: traversals and tree aggregations are O(n) time; recursive DFS/LCA/BST/balance use O(height) stack and can fail on long chains. Level order uses O(width) auxiliary queue space, excluding output. Serialization/deserialization are linear in token count plus encoded text size, with O(n) token storage and O(height) traversal stack. The LCA contract assumes both nodes exist; validate presence if the question does not guarantee it.

---

## 12. Graphs

### Build

```python
g = defaultdict(list)
for u, v in edges:
    g[u].append(v)
    g[v].append(u)               # omit for directed

# weighted
g[u].append((v, w))
```

**Explanation:** Clarify directed vs undirected in the first 30 seconds. Duplicate edges and self-loops: ask. If nodes are `1..n` not `0..n-1`, either allocate `n+1` or use dict keys. Weighted edges store tuples; don’t forget to unpack `(v, w)` in BFS/Dijkstra.

### Directions (grid)

```python
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
# 8-dir: add (1,1),(1,-1),(-1,1),(-1,-1)

def inb(r, c):
    return 0 <= r < R and 0 <= c < C
```

**Explanation:** Four-neighborhood is default (islands, maze). 8-dir only if the problem says diagonal. Bound-check **before** indexing or you throw. `R, C = len(grid), len(grid[0])` — guard empty grid (`if not grid or not grid[0]`).

### BFS (unweighted shortest path)

```python
def bfs(start):
    q = deque([start])
    dist = {start: 0}
    while q:
        u = q.popleft()
        for v in g[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

**Explanation:** Mark visited **when enqueueing**, not when dequeuing. If you mark late, the same node is queued many times (still correct for unweighted if you check, but slower; can explode). `dist` doubles as visited. First time you see a node is the shortest path in an unweighted graph. Use `deque.popleft`; `list.pop(0)` is a bug.

### 0-1 BFS (edges weight 0 or 1)

```python
dist = [math.inf] * n
dist[s] = 0
q = deque([s])
while q:
    u = q.popleft()
    for v, w in g[u]:
        nd = dist[u] + w
        if nd < dist[v]:
            dist[v] = nd
            (q.appendleft if w == 0 else q.append)(v)
```

**Explanation:** Dijkstra on weights `{0,1}` can be a deque: weight 0 = “same distance, process first” → `appendleft`; weight 1 = “+1, later” → `append`. This is O(V+E), not O(E log V). Use when: doors/walls cost 1, empty cells cost 0; or “stay vs move.” You may visit a node more than once if a better dist appears — that’s intended (`if nd < dist[v]`).

### Multi-source BFS (rotting oranges, walls & gates)

```python
def grid_distances(rows, cols, sources):
    # Nonnegative dimensions; valid source coordinates; all cells traversable.
    dist = [[-1] * cols for _ in range(rows)]
    q = deque()
    for r, c in sources:
        if dist[r][c] == -1:
            dist[r][c] = 0
            q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist  # -1 means unreachable, including when sources is empty
```

**Explanation:** “How long until all oranges rot?” is not n BFS runs. Put **every** rotten orange / gate in the queue at time 0. The wavefront expands simultaneously. Result is min time to each cell. If a fresh orange is never reached, return -1.

The supplied open-grid version costs O(rows × cols + number of supplied sources) time and O(rows × cols) space. Add a passability test when adapting it to walls or cells that must not be traversed.

### DFS grid / islands

```python
def grid_dfs(r, c):
    if not inb(r, c) or grid[r][c] != "1":
        return
    grid[r][c] = "0"
    for dr, dc in DIRS:
        grid_dfs(r + dr, c + dc)
```

**Explanation:** Mutating `'1'` → `'0'` marks globally visited land. To preserve the grid while counting islands, use a separate visited set or a copy. Do not restore cells after each island DFS: that makes the outer loop rediscover the same component. Restoration is for path backtracking such as word search. Long snake-shaped islands require iterative traversal.

```python
def count_islands(grid):
    # Rectangular grid of "0"/"1" strings. Does not mutate input.
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen, count = set(), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or (r, c) in seen:
                continue
            count += 1
            seen.add((r, c))
            stack = [(r, c)]
            while stack:
                x, y = stack.pop()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < rows and 0 <= ny < cols
                            and grid[nx][ny] == "1" and (nx, ny) not in seen):
                        seen.add((nx, ny))
                        stack.append((nx, ny))
    return count

def connected_components(graph):
    # Undirected adjacency list, vertex IDs 0..len(graph)-1.
    seen, count = set(), 0
    for start in range(len(graph)):
        if start in seen:
            continue
        count += 1
        seen.add(start)
        stack = [start]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
    return count
```

Island counting is expected O(rows × cols) time/space. Graph components are expected O(V+E) time/O(V) auxiliary space. Mark vertices when pushing to avoid duplicate stack entries. This component algorithm is not an SCC algorithm for directed graphs.

### Topological sort (Kahn)

```python
def topological_sort(n, edges):
    # Vertices 0..n-1; edge u->v means u precedes v.
    indeg, g = [0] * n, [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []
```

**Explanation:** Edge `u → v` means “u before v” (u is a prerequisite). Indegree 0 = no unmet prereq. Repeatedly take those. If you cannot order all n nodes, a cycle exists (course schedule returns `False`).

Kahn is BFS. DFS topo: 3-colors (see §21); push to output **after** exploring children, then reverse. Kahn is easier to get right under pressure.

O(V+E) time and space including graph construction. A nonempty graph returning `[]` has a cycle; an empty graph has a valid empty order. For a DAG, an order is unique only if there is exactly one available vertex at every step. Detect cycles before interpreting this uniqueness condition.

### Dijkstra

```python
def dijkstra(n, g, src):
    dist = [math.inf] * n
    dist[src] = 0
    h = [(0, src)]
    while h:
        d, u = heapq.heappop(h)
        if d != dist[u]:
            continue             # stale
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(h, (nd, v))
    return dist
```

**Explanation:** Use the Dijkstra guarantee for nonnegative weights. With negative edges, consider Bellman–Ford or an algorithm justified by additional structure, such as a DAG; clarify negative-cycle handling.

`if d != dist[u]: continue` drops outdated heap entries after a better path was found. Without it you still get correct dist if you only relax when `nd < dist[v]`, but you waste time.

The correctness/efficiency guarantee requires nonnegative weights. **Dijkstra does work with 0/1 weights**; 0–1 BFS is a faster specialized alternative. For unweighted shortest paths, ordinary BFS is simpler.

For this lazy heap implementation: O(V + E log(E+1)) time and O(V+E) auxiliary space, excluding the input graph. The common O((V+E) log V) bound uses the usual simple-graph setting. Vertices are integer IDs in `0..n-1`; unreachable distances remain `math.inf`.

State Dijkstra (cheapest flights with k stops): heap key is `(cost, node, stops)` and `dist` is 2D `[node][stops]` or you allow revisits with fewer stops.

### Union-Find (path compression + union by rank)

```python
class UF:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0] * n
        self.n = n               # component count

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1
        self.n -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)
```

Dynamic keys (accounts merge):

```python
class DynamicUF:
    def __init__(self):
        self.parent, self.size = {}, {}
        self.components = 0

    def find(self, x):
        # x must be hashable. Lazily add new keys.
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1
            self.components += 1
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True
```

**Explanation:** Each element starts as its own parent. `find` returns the root (component id). Path compression (`p[x] = p[p[x]]` or recursive `p[x] = find(p[x])`) flattens. Union by rank/size keeps trees shallow. Amortized ≈ O(α(n)) ≈ O(1).

`union` returns `False` if already connected — that edge is redundant (LC 684) or a cycle in an undirected graph.

`self.n` tracks component count: islands, provinces, “early stop Kruskal when n==1.”

**Kruskal MST:** sort edges by weight, union if not connected, add weight.

Dict version: nodes may be emails/strings. Iterative find plus union by size avoids recursive chains. After all unions, group existing keys by `uf.find(x)`. Both implementations have amortized O(α(n)) union/find cost under the usual constant/expected-constant-time storage assumptions, and O(n) space.

Don’t union by raw values without `find`: `p[a] = b` without roots is wrong.

---

## 13. Trie

```python
class TrieNode:
    def __init__(self):
        self.ch = {}
        self.end = False
        # self.idx = -1          # word index for Word Search II
        # self.refs = 0          # prune when a word is found

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        n = self.root
        for c in word:
            if c not in n.ch:
                n.ch[c] = TrieNode()
            n = n.ch[c]
        n.end = True

    def search(self, word: str) -> bool:
        n = self._walk(word)
        return bool(n and n.end)

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def _walk(self, s):
        n = self.root
        for c in s:
            if c not in n.ch:
                return None
            n = n.ch[c]
        return n
```

Wildcard (`.` = any): DFS from node.

**Explanation:** A tree of characters. Shared prefixes share nodes. `end=True` distinguishes `"app"` from prefix of `"apple"`.

`search` requires `end`; `startsWith` only requires the path exists.

**Word Search II:** put all words in a trie, DFS the board, walk the trie in lockstep. When `end`, record the word and set `end=False` (or delete the leaf) so you don’t duplicate. `refs` count lets you prune dead branches after a word is found.

**`.` wildcard:** from current node, if `c == '.'`, recurse into **all** children; else one child. That’s LC 211.

Array of 26 vs dict: dict is shorter and handles unicode; 26-array is faster for lowercase. Either is fine.

---

## 14. Backtracking template

```python
def permute(nums):
    n, res, used = len(nums), [], [False] * len(nums)
    def bt(path):
        if len(path) == n:
            res.append(path[:])
            return
        for i in range(n):
            if used[i]:
                continue
            # dup prune (sorted): if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue
            used[i] = True
            path.append(nums[i])
            bt(path)
            path.pop()
            used[i] = False
    bt([])
    return res

def subsets(nums):
    res = []
    def bt(i, path):
        if i == len(nums):
            res.append(path[:])
            return
        bt(i + 1, path)          # skip
        path.append(nums[i])     # take
        bt(i + 1, path)
        path.pop()
    bt(0, [])
    return res

# grid word search: mark visited in-place, restore
# board[r][c] = "#"; ...; board[r][c] = ch
```

**Explanation:** Backtracking = choose → recurse → **unchoose**. If you forget `path.pop()` / `used[i]=False`, later branches see a dirty state.

`res.append(path[:])` copies. `res.append(path)` stores a reference that will be mutated to empty.

**Permute:** `used` prevents picking the same **index** twice. For duplicate **values**, sort first and skip `nums[i]==nums[i-1] and not used[i-1]` (only the first copy can start a branch).

**Subsets:** each element has skip/take. Equivalent loop: at index `i`, append `nums[j]` for `j >= i`, recurse `j+1`. Combination-sum is subsets with reuse: recurse `i` not `i+1` when you may reuse `nums[i]`.

**Grid:** mark cell visited before 4-dir recurse, restore after. In-place `'#'` avoids a parallel `seen` matrix.

State output-sensitive complexity: permutations O(n·n!) in the distinct-value worst case; subsets O(n·2^n), including copies. Auxiliary path/stack space is O(n), excluding output. There is no universal n=12 cutoff: 13 elements have 8,192 subsets but 13! permutations. Judge output size and pruning.

---

## 15. DP snippets

```python
def coin_change(coins, amount):
    # Positive integer coins, nonnegative amount; unlimited reuse.
    dp = [math.inf] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for value in range(coin, amount + 1):
            dp[value] = min(dp[value], dp[value - coin] + 1)
    return -1 if dp[amount] == math.inf else dp[amount]

def house_robber(nums):
    # Nonadjacent elements; choosing none is permitted.
    two_back = one_back = 0
    for value in nums:
        two_back, one_back = one_back, max(one_back, two_back + value)
    return one_back

def max_subarray(nums):
    # A nonempty contiguous subarray is required.
    if not nums:
        raise ValueError("nonempty input required")
    ending = best = nums[0]
    for i in range(1, len(nums)):
        ending = max(nums[i], ending + nums[i])
        best = max(best, ending)
    return best

def lis_length(nums):
    tails = []
    for value in nums:
        i = bisect.bisect_left(tails, value)
        if i == len(tails):
            tails.append(value)
        else:
            tails[i] = value
    return len(tails)

def lcs(a, b):
    # Empty-prefix LCS values are ZERO.
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]

def edit_distance(a, b):
    # Unit-cost insertion, deletion, substitution.
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        dp[i][0] = i
    for j in range(len(b) + 1):
        dp[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[-1][-1]

def knapsack_01(weights, values, capacity):
    # Equal-length arrays; positive weights; capacity >= 0; may choose none.
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for room in range(capacity, weight - 1, -1):
            dp[room] = max(dp[room], dp[room - weight] + value)
    return dp[capacity]

def min_path_sum(grid):
    # Nonempty rectangular grid; right/down moves; negative costs allowed.
    if not grid or not grid[0]:
        raise ValueError("nonempty grid required")
    rows, cols = len(grid), len(grid[0])

    @lru_cache(None)
    def solve(r, c):
        if r == rows - 1 and c == cols - 1:
            return grid[r][c]
        best = math.inf
        if r + 1 < rows:
            best = min(best, solve(r + 1, c))
        if c + 1 < cols:
            best = min(best, solve(r, c + 1))
        return grid[r][c] + best

    return solve(0, 0)
```

**Explanation:** DP = state + transition + base + order.

**Say the state in one sentence:** “`dp[i]` = min coins to make amount i.” If you cannot, you don’t understand it yet.

**Unbounded knapsack (coin change):** outer coins, inner amount **ascending** so `dp[a - x]` already includes using this coin. **0-1 knapsack:** inner amount **descending** so you don’t reuse the same item.

**House robber:** the two-variable form preserves only the dependencies needed by the recurrence. Explain this space optimization; it is not a level-specific hiring signal.

**LIS tails:** `tails[k]` = smallest tail of any LIS of length k+1. Not the LIS itself. `bisect_left` finds the first tail ≥ x (strict LIS). For non-decreasing use `bisect_right`. Length is `len(tails)`; reconstructing the sequence needs extra parent pointers.

**LCS:** first row/column are zero because an empty sequence shares no elements. **Edit distance:** first row/column count insertions/deletions. These base cases are different. Both fill the remaining cells from already-computed prefixes.

**Tree DP:** return multiple values from a subtree (rob this node vs not). Don’t use a global `dp` indexed by node unless you have ids.

**Memoization:** `min_path_sum` caches hashable `(r, c)` arguments. Defining the cached function inside the public function isolates each call's grid. The grid must remain unchanged during the call. `@cache` is a Python 3.9+ shorthand; `@lru_cache(None)` supports the baseline here. Memoization removes repeated work but not recursion depth; use bottom-up DP for deep paths. [Python functools documentation](https://docs.python.org/3/library/functools.html#functools.cache)

| Template | Time | Auxiliary space |
|---|---|---|
| Coin change | O(number of coins × (amount+1)) | O(amount+1) |
| House robber / Kadane | O(n) | O(1) |
| Strict LIS length | O(n log(n+1)) | O(n) |
| LCS / edit distance | O((m+1)(n+1)) | O((m+1)(n+1)); can roll rows |
| 0/1 knapsack | O(items × (capacity+1)) | O(capacity+1) |
| Memoized right/down path | O(rows × cols) | O(rows × cols) cache plus O(rows+cols) stack |

---

## 16. Design: LRU (understand the map/list invariant)

```python
class CacheNode:
    def __init__(self, k=0, v=0):
        self.k, self.v = k, v
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("capacity must be nonnegative")
        self.cap = capacity
        self.m = {}
        self.head, self.tail = CacheNode(), CacheNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add(self, n):            # after head
        n.next = self.head.next
        n.prev = self.head
        self.head.next.prev = n
        self.head.next = n

    def _remove(self, n):
        n.prev.next = n.next
        n.next.prev = n.prev

    def get(self, key: int) -> int:
        if key not in self.m:
            return -1
        n = self.m[key]
        self._remove(n)
        self._add(n)
        return n.v

    def put(self, key: int, value: int) -> None:
        if key in self.m:
            self._remove(self.m[key])
        n = CacheNode(key, value)
        self.m[key] = n
        self._add(n)
        if len(self.m) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.m[lru.k]
```

`OrderedDict` version (say you know both; DLL shows more):

```python
from collections import OrderedDict
class OrderedLRUCache:
    def __init__(self, cap):
        if cap < 0:
            raise ValueError("capacity must be nonnegative")
        self.cap, self.d = cap, OrderedDict()
    def get(self, k):
        if k not in self.d:
            return -1
        self.d.move_to_end(k)
        return self.d[k]
    def put(self, k, v):
        if k in self.d:
            self.d.move_to_end(k)
        self.d[k] = v
        if len(self.d) > self.cap:
            self.d.popitem(last=False)
```

**Explanation:** Need O(1) get and O(1) put with eviction of **least recently used**. Hash map gives O(1) lookup; order needs a **doubly** linked list (singly cannot remove in O(1) without the predecessor).

Sentinel `head` / `tail` avoid empty-list edge cases. Convention: **MRU next to head**, **LRU next to tail** (or the reverse — pick one and stick to it). `get` and `put` both count as use → move node to MRU.

`put` on existing key: update value **and** recency. Evict only when `len > cap` **after** insert.

Store `k` on the node so eviction can `del self.m[lru.k]`.

**OrderedDict:** `move_to_end` marks MRU; `popitem(last=False)` removes LRU under this convention. Both versions have expected O(1) get/put and O(capacity) storage; zero capacity works. They return -1 for a missing key and are not thread-safe. If implementing internals is the task, use the linked-list version; otherwise confirm whether library primitives are acceptable. Distinct class names prevent overwriting the graph `Node` or the other cache example.

---

## 17. Strings / parsing

```python
s.split()                        # whitespace, strips extras
s.split(",")
list(s)                          # chars
ord("a"); chr(97)
s.isalpha(); s.isdigit(); s.isalnum()
s.lower()
"".join(chars)
s[::-1]                          # reverse
s[i:j]                           # slice, safe if j > len
# rotate: s[k:] + s[:k]

# calculator / stack
# signs, prev operator, accumulating num
# decode string: two stacks (counts, strings) or recursion

# integer from stream
num = 0
for ch in s:
    if "0" <= ch <= "9":        # ASCII digit contract
        num = num * 10 + int(ch)

# avoid eval()
```

**Explanation:** Strings are immutable. Repeated concatenation can require O(n²) copying; do not rely on interpreter-specific optimizations. Append to a list and join once.

`split()` with no args collapses whitespace and strips; `split(" ")` does **not** (keeps empty tokens). Know which you want.

`s[i:j]` never throws IndexError; out-of-range just shortens. `s[i]` **does** throw.

**Parse integers** yourself in calculator problems: `num = num*10 + int(ch)`, then on an operator flush `num`. Don’t `eval`.

The small loop above extracts ASCII digits; a full calculator must flush/reset on operators. `isdigit()` accepts characters such as `²` that `int()` cannot parse. If Unicode decimal digits are part of the contract, use an appropriate classification such as `isdecimal()`. [Python character classification](https://docs.python.org/3/library/stdtypes.html#str.isdigit)

**Basic calculator:** stack of signs / previous results when you see `(`. One sign variable, one total, one `num`.

**Decode string (`3[a2[c]]`):** when you see `[`, push current string and count; when `]`, pop and repeat. Nested encoding is a stack, not regex.

`ord(ch) - ord('a')` → 0..25 index. Guard non-lowercase if the problem allows it.

---

## 18. Math / bits / random

```python
math.inf; -math.inf              # prefer over 10**18 unless stated
math.gcd(a, b)
math.lcm(a, b)                   # 3.9+
-(-a // b)                       # exact ceiling division for integer a, b > 0
abs(x); pow(x, n, mod)           # modular exponent

# bits
x & 1; x >> 1; x << 1
x & (x - 1)                      # drop lowest set bit
x & -x                           # lowest set bit
bin(x).count("1")                # popcount
# x.bit_count()                 # Python 3.10+; counts bits of abs(x)
# set/clear/toggle bit i:  x | (1<<i);  x & ~(1<<i);  x ^ (1<<i)

import random
random.randrange(n)              # [0, n)
# reservoir sampling: P(keep i) = k / seen_count
```

**Explanation:** Python integers have arbitrary precision, subject to memory. Operations on increasingly large integers are not constant-time. Use `math.inf` for an unreachable distance rather than an arbitrary finite cutoff.

**Ceiling division:** for integer a and positive b, `-(-a // b)` is exact even for negative a. Avoid `/` when an exact integer quotient is required: `int((10**18 + 1) / 1)` loses the last unit.

```python
def trunc_div(a, b):
    # Integers, b != 0: divide toward zero without floating point.
    quotient = abs(a) // abs(b)
    return -quotient if (a < 0) != (b < 0) else quotient

def ceil_div(a, b):
    # Integers, b > 0.
    return -(-a // b)
```

`pow(x, n, mod)` is fast modular exponent (fast pow). Don’t write your own unless asked.

**Bits:** for positive x, `x & (x-1)` clears its lowest set bit, and `x & -x` isolates it. Use nonnegative masks; Python negative integers have sign-extended bitwise semantics, so a clear-lowest-bit loop does not terminate on them. Determine feasibility of subset/bitmask work from O(2^n) states and per-state work, not a company-specific frequency claim.

**Reservoir sampling:** stream of unknown length, keep k items uniformly. For k=1: replace current with item i with probability `1/i`. Say this if they ask “what if the list doesn’t fit in memory.”

`random.choice` / `randrange` for “insert-delete-getrandom”: store values in a list + dict index; delete = swap with last, pop (O(1)).

---

## 19. itertools (use when it saves 10 lines)

```python
itertools.accumulate(a)          # prefix sums
itertools.pairwise(a)            # (a[i], a[i+1])  3.10+
itertools.permutations(a, r)
itertools.combinations(a, r)
itertools.product(range(R), range(C))   # all cells
itertools.chain.from_iterable(list_of_lists)
itertools.groupby(sorted(s))     # consecutive groups; SORT FIRST
```

**Explanation:** Interviewers accept these if you can explain them. Don’t hide an O(n!) bomb inside `permutations` for n=10 without saying so.

`groupby` only groups **consecutive** equal keys. Sort first, or you get split groups. Each group is an iterator — materialize with `list(g)` if you need it twice.

`product` is nested loops: `product(range(R), range(C))` = all cells. `repeat=n` for binary strings of length n (n≤20).

Prefer explicit loops if the interviewer is old-school; use itertools when it removes nesting.

---

## 20. Matrix / flatten tricks

```python
R = len(grid)
C = len(grid[0]) if R else 0     # rectangular input
matrix = [[0] * C for _ in range(R)]
# WRONG: matrix = [[0] * C] * R  # every row aliases the same inner list
grid = [row[:] for row in grid] # independent rows; mutable cell objects still shared
# flatten index: id = r * C + c;  r, c = divmod(id, C)
# transpose: list(map(list, zip(*grid)))
# rotate 90 CW: reverse rows then transpose — or transpose then reverse each row
```

**Explanation:** `grid[:]` copies the outer list only; inner rows are still shared. Mutating `grid[0][0]` would hit the original. Row-copy with `row[:]`.

Create independent rows with a comprehension as shown. For scalar cells this is sufficient; nested mutable cell objects require deeper copying if their internals must be independent.

Flatten when you need UF on a grid: node id = `r*C + c`. Reverse with `divmod`.

**Rotate 90 CW:** `list(map(list, zip(*grid[::-1])))`. **CCW:** `list(map(list, zip(*grid)))[::-1]`. These return new matrices. Draw a 2×2 example to confirm direction.

Empty grid: `len(grid[0])` throws. Guard.

---

## 21. Recursion / graph coloring visited

```python
def has_directed_cycle(graph):
    # Adjacency list with IDs 0..n-1; explicit DFS stack avoids recursion depth.
    color = [0] * len(graph)  # 0 unvisited, 1 active, 2 finished
    for start in range(len(graph)):
        if color[start] != 0:
            continue
        color[start] = 1
        stack = [(start, iter(graph[start]))]
        while stack:
            u, neighbors = stack[-1]
            v = next(neighbors, None)  # vertex IDs are ints, never None
            if v is None:
                color[u] = 2
                stack.pop()
            elif color[v] == 1:
                return True
            elif color[v] == 0:
                color[v] = 1
                stack.append((v, iter(graph[v])))
    return False

def is_bipartite(graph):
    # Undirected adjacency list; handles disconnected components and self-loops.
    color = [0] * len(graph)
    for start in range(len(graph)):
        if color[start] != 0:
            continue
        color[start] = 1
        q = deque([start])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if color[v] == color[u]:
                    return False
                if color[v] == 0:
                    color[v] = -color[u]
                    q.append(v)
    return True
```

**Explanation:** Boolean visited cannot detect **back-edges to the current path** (cycle in directed graphs). Colors:

- 0 = never seen
- 1 = on the DFS stack (gray)
- 2 = finished (black)

If you walk to a gray node → cycle. Walk to black → already processed, skip.

Grid cells as `seen.add((r, c))` — tuples are hashable, lists are not.

Both graph functions use O(V+E) time and O(V) auxiliary space. Directed DFS colors track progress; bipartite colors track two disjoint vertex groups. These are different uses of coloring.

If the state is a **set of collected keys** (shortest path to get all keys), the dict key is `(r, c, bitmask)` or `frozenset`. Bitmask is faster: `state | (1 << key_id)`.

---

## 22. Complexity one-liners (say before coding)

| Structure | Get | Add | Notes |
|---|---|---|---|
| `list` | O(1) idx | O(1) am | `pop(0)` is O(n) — use `deque` |
| `deque` | O(1) ends | O(1) ends | BFS, sliding window max (monotonic) |
| `dict` / `set` | avg O(1) | avg O(1) | keys must be hashable (`tuple`, `frozenset`) |
| `heapq` | O(1) peek | O(log n) | min-heap; negate for max |
| `bisect` | O(log n) | O(n) insert | array must stay sorted |
| `sort` | — | O(n log n) | Timsort, stable |

As rough starting points, large arrays often need O(n) or O(n log n), while small state spaces may allow quadratic or exponential work. Estimate actual operations, output size, interpreter overhead, and the time limit; these are not universal n cutoffs.

**Explanation:** State time and auxiliary space, including expected/amortized qualifications. Hashing long strings and large integers also has a cost. If input bounds are missing, clarify them before choosing the algorithm.

Amortized `list.append` is O(1). Insert at index 0 is O(n).

Space: recursion uses O(height) stack. BFS uses O(width). Mention both.

---

## 23. Python gotchas that fail interviews

```python
# 1. Mutable default
# def f(a=[]): ...    # BAD: list created once, shared across calls
def f(a=None):
    if a is None:
        a = []

# 2. Copy
b = a[:]              # shallow list
b = [row[:] for row in a]
import copy; copy.deepcopy(obj)   # rare; usually don’t need

# 3. `is` vs `==`
# is → identity (None: `if x is None`)
# == → value

# 4. Hashable keys
# list/set/dict cannot be keys; tuple/frozenset members must themselves be hashable

# 5. Integer division
5 / 2 == 2.5
5 // 2 == 2             # floor (towards -inf): (-5)//2 == -3
trunc_div(a, b)         # exact toward zero; helper in section 18, b != 0

# 6. Sorting mixed types / None — will throw. Filter first.

# 7. Inspect sys.getrecursionlimit(); use iterative traversal for deep chains.

# 8. `for i in range(len(a)):` mutating a while iterating — iterate copy or index carefully.

# 9. `and`/`or` return operands, not bool:
# [] or [1] → [1]

# 10. Don’t use `list` as visited for O(n) membership; use set.

# 11. `Counter - Counter` drops non-positive keys. Fine for anagram remainder.

# 12. True, False, None are singletons; 1 == True, but 1 is not True.
```

**Explanation:** These are the bugs that make a correct algorithm look broken.

1. Default `[]` is created **once** at function def. Second call sees leftover data.
2. `b = a` aliases. `a[:]` copies one level. Nested lists need a comprehension or you mutate the original grid.
3. `if x:` is false for `0`, `[]`, `""`. Use `if x is None` when 0 is valid.
4. `seen.add([r,c])` TypeError. `tuple` / `frozenset`.
5. `//` floors toward −∞. For mid of negatives in binary search this still works for indices ≥ 0. Don’t use `/` then `int` for index math.
7. Linked-list reverse should **not** be recursive on 10^5. Same for skewed trees.
8. `for x in a: a.remove(x)` skips elements. Iterate `a[:]` or collect to-delete.
9. `x = d.get(k) or []` silently substitutes `[]` for valid falsey values such as `0` or `""`. Use `if k not in d` when absence is the condition.
10. Repeated membership checks in a length-n list can make an n-iteration loop O(n²). Use a set when its semantics fit.
12. `True == 1`; `Counter` / dict can surprise you if you mix bool and int keys. Don’t.

---

## 24. Live-interview typing order (every problem)

```python
class Solution:
    def solve(self, nums: List[int]) -> int:
        # Signature and empty-input behavior depend on the actual question.
        raise NotImplementedError("Replace this scaffold after clarifying the contract")
```

Use this sequence, adapting the scaffold only after clarification:
1. restate + constraints (`n` size)
2. brute + complexity
3. name pattern
4. code
5. dry-run the example
6. edges: `[]`, `n==1`, duplicates, negatives, disconnected, cycle
7. time / space aloud

**Explanation:** Confirm the signature and empty-input behavior before implementing. Do not automatically return 0: the contract may require an empty list, None, an exception, or another value. Explain the model before naming a pattern.

Dry-run an example aloud and deliberately test relevant boundaries. Make your reasoning and validation visible rather than depending on the interviewer to request them.

If stuck 5 minutes: drop to brute, then optimize. A slow correct solution beats a clever half-wrong one.

---

## 25. Rotating recall drills

Rotate **two or three** items per 15–25-minute session. The full list is a multi-session checklist, not a ten-minute typing requirement:

1. BFS + grid `DIRS` + `inb`
2. Dijkstra with stale-skip
3. Union-Find
4. Binary search on answer
5. LRU (DLL + dict)
6. Trie insert/search
7. Reverse linked list + dummy
8. Tree level-order + iterative inorder
9. Topo Kahn
10. Sliding window min/max template
11. Heap max via negate + tuple tie-break
12. Merge intervals

If a basic template is slow or buggy, practise it again in a later session. Scale time to its complexity; a cache implementation and a heap call are not equivalent drills.

**Explanation:** Use these sessions for retrieval during the preparation weeks. On interview morning, keep review light: inspect your personal error log and rehearse one familiar example. Avoid a full template marathon or new difficult topics.

Talk while you type the drill once: that is the same muscle as the real loop.
