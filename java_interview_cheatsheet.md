# Java interview snippets: Google L4 / L5 preparation

This is your Java DSA reference for the 12-week preparation plan: **53 snippet groups**, with standard-library usage, reusable algorithms, assumptions, and complexity notes. The earlier plan recommended Python; this reference supports Java if you choose it. Practise in one primary language after your baseline comparison.

**Scope:** coding interviews and small data-structure design exercises. This is a strong working toolkit, not an exhaustive catalogue of algorithms or a prediction of interview questions. Spring, JPA, JVM tuning, and production concurrency deserve separate preparation if your confirmed interview includes those topics.

**Compatibility:** Java 8 language/API baseline, checked with `javac --release 8` on JDK 25. Avoid relying on records, `var`, `List.of`, or newer collection APIs unless the interview runtime supports them.

**Use before the interview:** reconstruct these from a blank editor, explain the invariant, and test a boundary case. During the actual interview, follow the permitted-resource rules; this is a preparation reference.

## How to prioritize

| Priority | What to do |
|---|---|
| Essential | Be able to write the basic form fluently, explain correctness, and adapt it. |
| Important | Understand the mechanism and practise implementing it; do not merely memorize lines. |
| Stretch | Study after the fundamentals are reliable. These are useful when constraints justify them. |

**First pass:** collections and syntax (01–08), binary search (10–11), prefix sums (12), windows (14–15, 44), tree traversals (20–22), graphs (23–27, 47), and DP (30–32).

**Second pass:** linked lists (09, 43, 51), heaps, intervals, backtracking (29, 53), tries, monotonic structures, LIS, LRU, knapsack, bipartite coloring, 0-1 BFS (46), serialize (48), edit distance (49), and decode-string (50). Treat snippets 35–36 as stretch work.

**For L5:** knowing more templates does not establish senior scope. Continue system design and leadership preparation alongside these drills.

## Ten-second pattern selection

| Clue in the problem | Candidate pattern | Check before committing |
|---|---|---|
| Sorted values; locate first/last occurrence | Lower/upper bound (10) | Ascending order and half-open bounds |
| Minimum feasible capacity/speed | Binary search on answer (11) | Feasibility must be monotone |
| Subarray sum equals a target; negatives allowed | Prefix sum + frequency map (12) | Seed the empty prefix; count before insertion |
| Longest substring with at most k distinct symbols | Variable window (14) | Shrinking must restore validity monotonically |
| Smallest window covering all required characters | Minimum covering window (44) | Count satisfied unique requirements, not raw frequencies |
| Every window has fixed width | Running sum or monotonic deque (15, 17) | Expire old indices; decide how ties behave |
| Next larger/smaller value | Monotonic stack (16) | Strict versus non-strict comparison |
| Overlap or concurrency | Sort intervals; heap/sweep reasoning (18–19) | Closed versus half-open endpoints |
| Tree aggregation from children | Postorder recursion (21) | Meaning of each return value and stack depth |
| Fewest edges in an unweighted graph | BFS (23–24) | Mark visited when enqueuing |
| Grid components / islands | Iterative grid DFS (47) | Mark visited when pushing; use a copy or separate visited set to preserve the grid |
| Edge weights only 0 or 1 | 0-1 BFS (46) | `offerFirst` on 0, `offerLast` on 1; Dijkstra is also valid but less specialized |
| Dependencies and scheduling | Topological sort (25) or DFS 3-color (52) | Edge direction; detect a cycle |
| Nonnegative weighted shortest path | Dijkstra (26) | Reject negative weights; skip stale entries |
| Repeated connectivity / incremental undirected edges | Union-find (27) | Does not support arbitrary deletions directly |
| Prefix lookup | Trie (28) | Alphabet and memory footprint |
| Enumerate valid choices | Backtracking (29, 53) | Restore state and copy completed paths |
| Nested encoded strings / calculators | Stack parse (50) | Push on `[` / `(`, flush number before the operator |
| Reconstruct a tree from a string | Serialize with null sentinels (48) | Null markers make preorder 1-1 |
| Repeated subproblems with well-defined state | DP (30–32, 39–40, 49) | State, recurrence, base case, evaluation order |
| Submatrix sums / many range increments | 2D prefix or difference array (45) | Inclusive vs half-open index convention |
| Repeated point updates and range sums | Fenwick tree (36) | Zero-based public interface; half-open ranges |
| Constant-time recency cache | Hash map + doubly linked list (41) | Maintain map/list consistency |

## Standard-library complexity to say aloud

| Operation | Practical bound / caveat |
|---|---|
| Array indexed access | O(1) |
| Array copy, fill, equality scan | O(n) worst case |
| ArrayList get/set | O(1) |
| ArrayList append | Amortized O(1) |
| ArrayList insert/remove at an arbitrary index | O(n) because elements move |
| HashMap/HashSet lookup, insert, remove | Expected O(1) with well-distributed hashes; hashing/comparing a long string is additional work |
| TreeMap/TreeSet lookup, insert, remove, boundary search | O(log n) for these implementations |
| ArrayDeque operations at either end | Amortized O(1); searching/removing a particular object is O(n) |
| PriorityQueue offer/poll | O(log n) |
| PriorityQueue peek | O(1) |
| PriorityQueue contains/remove(Object) | O(n); heap iteration is not sorted |
| General comparison sorting | Budget O(n log n); auxiliary space and worst-case details depend on the implementation and overload |
| StringBuilder append | Amortized O(1) per appended character; final string creation costs O(n) |

The API behaviors for deques, heaps, array utilities, and ordered maps are documented by Oracle: [ArrayDeque](https://docs.oracle.com/javase/8/docs/api/java/util/ArrayDeque.html), [PriorityQueue](https://docs.oracle.com/javase/8/docs/api/java/util/PriorityQueue.html), [Arrays](https://docs.oracle.com/javase/8/docs/api/java/util/Arrays.html), [TreeMap](https://docs.oracle.com/javase/8/docs/api/java/util/TreeMap.html). String indexing uses UTF-16 code units: [String](https://docs.oracle.com/javase/8/docs/api/java/lang/String.html).

## Java traps to eliminate before interview day

1. **Compare values correctly:** `s.equals(t)` / `Objects.equals(s,t)` for strings; boxed integers also need value comparison. `==` on node references is appropriate when identifying the same node.
2. **Cast before arithmetic:** `(long) a * b`, not `(long) (a * b)`. Use `Integer.compare` / `Long.compare` in comparators.
3. **Avoid accidental null unboxing:** `int x = map.get(key)` fails if the key is absent. Use a checked lookup or `getOrDefault`.
4. **Know all three lengths:** `array.length`, `string.length()`, `collection.size()`.
5. **Beware `List<Integer>.remove`:** `remove(1)` removes index 1; `remove(Integer.valueOf(1))` removes value 1.
6. **Understand array identity:** `int[]` keys do not compare by contents. Use a value key such as `Cell`, a suitable immutable list, or an unambiguous encoding.
7. **Avoid shared mutable snapshots:** `result.add(new ArrayList<>(path))`; a two-dimensional array's `clone()` copies only the outer array.
8. **Do not enqueue null into ArrayDeque.** Check tree children before adding them.
9. **Do not assume heap iteration is ordered or heap-key mutation is safe.** Poll entries and use a stale-entry check for updated priorities.
10. **Do not confuse visited with fully processed.** BFS discovery, DFS recursion-stack state, and Dijkstra's best distance mean different things.
11. **Do not apply a sum-based shrinking window blindly to negative numbers.** Prefix sums often work where that monotonicity fails.
12. **Keep interval conventions explicit.** For half-open meetings, an end at t frees the room for a start at t; closed overlapping intervals use different comparisons.
13. **Plan for recursion depth.** Java does not guarantee tail-call optimization; a long chain can cause `StackOverflowError`. Be able to use an explicit stack.
14. **Keep mutable per-call state local.** A reused `Solution` instance should not retain the previous invocation's result, visited set, or memo table accidentally.
15. **Use `long` for distances, prefix sums, and counts when needed.** `long` can also overflow; establish bounds rather than assuming it is unlimited.
16. **Respect the alphabet.** `c - 'a'` assumes lowercase English; `char` and code point are not interchangeable with a user-perceived character.
17. **Remember regex semantics:** `split("\\.")` splits on a literal dot, and the default split discards trailing empty fields.
18. **Understand Java parameter passing:** Java passes values, including object-reference values. Changing `node.next` affects the object; assigning a new object to the local parameter does not reassign the caller's variable. Return the new head/root when needed.
19. **Do not mutate equality/hash fields of a key already in a map or set.** Immutable key fields avoid losing access to entries.
20. **Do not structurally mutate a collection during an enhanced for-loop.** Use an iterator's supported remove operation or a separate update pass.

## Working files and verification

- [Compilable source](/Users/apoorvdubey/Study/prep_for_google/JavaInterviewTemplates.java)
- [Verification harness](/Users/apoorvdubey/Study/prep_for_google/JavaInterviewTemplatesTest.java)
- [Your 12-week plan](/Users/apoorvdubey/Study/prep_for_google/codex_proposed_plan.md)

Snippets 01–42 are extracted from the compilable source. Snippets 43–53 are maintained directly in this Markdown file and were extracted separately for the review described below. The linked Java source and harness still cover 01–42 only. Place methods and nested classes inside a class with `import java.util.*;`. When adapting a snippet to an interview platform's `Solution`, adjust the signature and node definitions to the provided ones. You do not need to paste the entire reference.

Compile and rerun the original 01–42 harness from the workspace:

```sh
cd /Users/apoorvdubey/Study/prep_for_google
javac --release 8 -Xlint:all,-options -d /private/tmp/codex-java-interview-check JavaInterviewTemplates.java JavaInterviewTemplatesTest.java
java -cp /private/tmp/codex-java-interview-check JavaInterviewTemplatesTest
```

On an actual JDK 8 installation, omit `--release 8` (that option was added later).

**Earlier verification, 01–42:** 52,260 checks passed, including explicit boundary examples and randomized comparisons against brute-force array algorithms, Floyd–Warshall shortest paths, graph reachability, and a simple LRU model.

**Review of 43–53, 7 September 2026:** All 53 Markdown snippets were extracted and compiled together using `javac --release 8 -Xlint:all,-options` on JDK 25. Sections 43–53 passed **24,786 checks** covering linked-list transformations, brute-force minimum windows and submatrix sums, difference-array updates, 0–1 BFS against Floyd–Warshall, islands against BFS, tree codec round trips, exhaustive small edit distances, generated nested decodings, merge-k, directed cycles, and word-search path enumeration. The `'#'` word-search collision and repeat-count overflow regressions were included. Recursive tree codecs and directed DFS remain explicitly limited by call-stack depth.

These checks are not a proof for every input. Respect each contract, including non-null inputs unless stated otherwise, valid vertex IDs, integer bounds, and the declared character alphabet. The commands above rerun the original harness, not the separate Markdown review checks.

## Snippet index

- [01. Arrays and lists](#snippet-01) — Essential
- [02. Strings and characters](#snippet-02) — Essential
- [03. HashMap and HashSet](#snippet-03) — Essential
- [04. Queue stack and deque](#snippet-04) — Essential
- [05. Heaps comparators and top-k](#snippet-05) — Essential
- [06. Ordered maps sets and multisets](#snippet-06) — Essential
- [07. Numeric safety and bit operations](#snippet-07) — Essential
- [08. Node definitions](#snippet-08) — Essential
- [09. Linked-list reverse cycle and merge](#snippet-09) — Essential
- [10. Binary-search boundaries](#snippet-10) — Essential
- [11. Binary search on the answer](#snippet-11) — Essential
- [12. Prefix sums and subarray-sum counting](#snippet-12) — Essential
- [13. Two pointers on sorted input](#snippet-13) — Essential
- [14. Variable sliding window](#snippet-14) — Essential
- [15. Fixed sliding window](#snippet-15) — Essential
- [16. Monotonic stack](#snippet-16) — Essential
- [17. Monotonic deque for sliding maximum](#snippet-17) — Important
- [18. Merge intervals](#snippet-18) — Essential
- [19. Meeting rooms and endpoint semantics](#snippet-19) — Important
- [20. Tree inorder and level-order traversal](#snippet-20) — Essential
- [21. Tree recursion balance and LCA](#snippet-21) — Essential
- [22. Validate a BST with bounds](#snippet-22) — Essential
- [23. Graph construction DFS and BFS distances](#snippet-23) — Essential
- [24. Grid and multi-source BFS](#snippet-24) — Essential
- [25. Topological sort and directed cycle detection](#snippet-25) — Essential
- [26. Dijkstra with stale-entry skipping](#snippet-26) — Essential
- [27. Union-find with size and path compression](#snippet-27) — Essential
- [28. Trie insert search and prefix](#snippet-28) — Essential
- [29. Backtracking subsets and unique permutations](#snippet-29) — Essential
- [30. Bottom-up DP coin change](#snippet-30) — Essential
- [31. Two-dimensional DP longest common subsequence](#snippet-31) — Essential
- [32. Top-down memoization](#snippet-32) — Essential
- [33. Longest increasing subsequence](#snippet-33) — Important
- [34. Merge sort](#snippet-34) — Important
- [35. Randomized three-way quickselect](#snippet-35) — Stretch
- [36. Fenwick tree for point updates and range sums](#snippet-36) — Stretch
- [37. LRU cache using library primitives](#snippet-37) — Important
- [38. Immutable composite hash-map key](#snippet-38) — Important
- [39. Kadane maximum subarray](#snippet-39) — Essential
- [40. One-dimensional 0-1 knapsack](#snippet-40) — Important
- [41. LRU internals hash map and doubly linked list](#snippet-41) — Important
- [42. Bipartite graph coloring](#snippet-42) — Important
- [43. Linked-list dummy, middle, reverse-k](#snippet-43) — Essential
- [44. Minimum covering window](#snippet-44) — Essential
- [45. 2D prefix sums and difference array](#snippet-45) — Important
- [46. 0-1 BFS](#snippet-46) — Important
- [47. Grid DFS islands](#snippet-47) — Essential
- [48. Serialize and deserialize a binary tree](#snippet-48) — Important
- [49. Edit distance](#snippet-49) — Important
- [50. Decode string](#snippet-50) — Important
- [51. Merge k sorted lists](#snippet-51) — Important
- [52. Directed cycle detection, DFS 3-color](#snippet-52) — Important
- [53. Grid word search](#snippet-53) — Important

<a id="snippet-01"></a>

## 01. Arrays and lists

**Priority: Essential.**

```java
static void arraysAndLists() {
    int[] a = {3, 1, 2};
    int[] copy = a.clone();
    int[] slice = Arrays.copyOfRange(a, 0, 2); // [0, 2)
    Arrays.sort(copy);                          // mutates copy
    int[] filled = new int[5];
    Arrays.fill(filled, -1);
    int[][] matrix = new int[2][3];
    for (int[] row : matrix) Arrays.fill(row, -1);
    int[][] deepCopy = new int[matrix.length][];
    for (int i = 0; i < matrix.length; i++) deepCopy[i] = matrix[i].clone();
    boolean equal = Arrays.equals(a, copy);
    boolean deepEqual = Arrays.deepEquals(matrix, deepCopy);
    List<Integer> list = new ArrayList<>(Arrays.asList(3, 1, 2));
    list.add(4);
    list.remove(Integer.valueOf(1)); // remove value 1
    list.remove(0);                 // remove index 0
    Collections.sort(list);
    Collections.reverse(list);
    Integer[] boxed = list.toArray(new Integer[0]);
    int[] primitive = list.stream().mapToInt(Integer::intValue).toArray();
    // Arrays.asList(new int[]{1, 2}) is a List<int[]> containing ONE array.
    // Arrays.asList(1, 2) is fixed-size; wrap in ArrayList to add/remove.
    // a.length; list.size(); Arrays.toString(a); Arrays.deepToString(matrix).
}
```

<a id="snippet-02"></a>

## 02. Strings and characters

**Priority: Essential.**

```java
static String stringTools(String s) {
    int n = s.length();
    if (n > 0) {
        char first = s.charAt(0);
        String rest = s.substring(1); // valid even when n == 1
        String prefix = s.substring(0, Math.min(3, n)); // end exclusive
    }
    char[] chars = s.toCharArray();
    Arrays.sort(chars);
    String sorted = new String(chars);
    String[] words = s.trim().isEmpty() ? new String[0] : s.trim().split("\\s+");
    String[] dotted = "a.b.".split("\\.", -1); // regex; preserve trailing empty
    boolean equal = Objects.equals(s, sorted); // null-safe equality
    int comparison = s.compareTo(sorted);     // lexicographic order
    StringBuilder out = new StringBuilder();
    for (char c : s.toCharArray()) out.append(c);
    if (out.length() > 0) out.deleteCharAt(out.length() - 1);
    return out.reverse().toString();
    // String is immutable. Repeated concatenation in a loop can be quadratic.
    // char is a UTF-16 code unit; use s.codePoints().toArray() if required.
    // Lowercase-English counting only: int[] count = new int[26]; count[c-'a']++.
}
```

<a id="snippet-03"></a>

## 03. HashMap and HashSet

**Priority: Essential.**

```java
static Map<Integer, Integer> frequencies(int[] a) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int x : a) freq.put(x, freq.getOrDefault(x, 0) + 1);
    // Equivalent increment: freq.merge(x, 1, Integer::sum);
    Set<Integer> seen = new HashSet<>();
    for (int x : a) {
        if (!seen.add(x)) { /* x was already present */ }
    }
    Map<String, List<Integer>> groups = new HashMap<>();
    groups.computeIfAbsent("key", k -> new ArrayList<>()).add(7);
    for (Map.Entry<Integer, Integer> entry : freq.entrySet()) {
        int value = entry.getKey(), count = entry.getValue();
    }
    // Decrement and remove zero counts (when x is present):
    // int next = freq.get(x) - 1;
    // if (next == 0) freq.remove(x); else freq.put(x, next);
    // Use iterator.remove() to remove during iteration.
    return freq;
}
```

<a id="snippet-04"></a>

## 04. Queue stack and deque

**Priority: Essential.**

```java
static void dequeTools() {
    Queue<Integer> queue = new ArrayDeque<>();
    queue.offer(10);
    Integer head = queue.peek(); // null if empty
    Integer removed = queue.poll();
    Deque<Integer> stack = new ArrayDeque<>();
    stack.push(10);
    int top = stack.peek();     // unboxing null would throw if empty
    int popped = stack.pop();   // throws if empty
    Deque<Integer> deque = new ArrayDeque<>();
    deque.offerFirst(1);
    deque.offerLast(2);
    deque.peekFirst();
    deque.peekLast();
    deque.pollFirst();
    deque.pollLast();
    // ArrayDeque rejects null. Keep queue and stack conventions distinct.
}
```

<a id="snippet-05"></a>

## 05. Heaps comparators and top-k

**Priority: Essential.**

```java
static int kthLargestHeap(int[] a, int k) {
    if (k < 1 || k > a.length) throw new IllegalArgumentException("k");
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    for (int x : a) {
        minHeap.offer(x);
        if (minHeap.size() > k) minHeap.poll();
    }
    return minHeap.peek(); // O(n log(k+1)) time, O(k) space
}
static void comparatorTools() {
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
    PriorityQueue<int[]> byCost = new PriorityQueue<>((a, b) -> {
        int cmp = Integer.compare(a[1], b[1]);
        return cmp != 0 ? cmp : Integer.compare(a[0], b[0]);
    });
    int[][] intervals = {{2, 4}, {1, 5}, {1, 3}};
    Arrays.sort(intervals, (a, b) -> {
        int cmp = Integer.compare(a[0], b[0]);
        return cmp != 0 ? cmp : Integer.compare(a[1], b[1]);
    });
    // Never use a[0] - b[0] as a comparator: overflow can break ordering.
    // Primitive int[] cannot take a comparator; int[][] can (rows are objects).
    // Heap iteration is NOT sorted. Repeated poll() retrieves sorted order.
    // Do not mutate a queued element's priority; reinsert a new entry instead.
}
```

<a id="snippet-06"></a>

## 06. Ordered maps sets and multisets

**Priority: Essential.**

```java
static void orderedTools() {
    TreeMap<Integer, Integer> counts = new TreeMap<>();
    counts.merge(10, 1, Integer::sum);
    counts.merge(10, 1, Integer::sum); // frequency 2
    counts.merge(20, 1, Integer::sum);
    Integer floor = counts.floorKey(15);   // <= 15
    Integer ceiling = counts.ceilingKey(15); // >= 15
    Integer lower = counts.lowerKey(10);   // < 10; null here
    Integer higher = counts.higherKey(10); // > 10
        int smallest = counts.firstKey(); // requires nonempty map
        int largest = counts.lastKey();
        int x = 10;
        Integer count = counts.get(x); // never unbox get() directly; absent => null
        if (count != null) {
            if (count == 1) counts.remove(x);
            else counts.put(x, count - 1);
        }
    NavigableSet<Integer> set = new TreeSet<>();
    set.add(10); set.add(20);
    Integer candidate = set.ceiling(11);
    // TreeSet removes duplicates according to its comparator (compare == 0).
}
```

<a id="snippet-07"></a>

## 07. Numeric safety and bit operations

**Priority: Essential.**

```java
static long gcd(long a, long b) { // nonnegative inputs
    while (b != 0) { long remainder = a % b; a = b; b = remainder; }
    return a;
}
static long modPow(long base, long exponent, int mod) {
    // exponent >= 0, mod > 0; int modulus keeps products within long range.
    long result = 1 % mod;
    base = Math.floorMod(base, (long) mod);
    while (exponent > 0) {
        if ((exponent & 1L) != 0) result = result * base % mod;
        base = base * base % mod;
        exponent >>= 1;
    }
    return result;
}
static void numericTools() {
    int a = Integer.MAX_VALUE, b = 2;
    long product = (long) a * b; // cast BEFORE arithmetic
    long sum = (long) a + b;
    long absolute = Math.abs((long) Integer.MIN_VALUE);
    long n = 15, d = 4; // n >= 0, d > 0
    long ceilDiv = n / d + (n % d == 0 ? 0 : 1); // no n+d overflow
    int normalized = Math.floorMod(-3, 5);
    int mask = 12, bit = 2; // 0 <= bit < 32 for int
    boolean isSet = (mask & (1 << bit)) != 0;
    int set = mask | (1 << bit), clear = mask & ~(1 << bit);
    int toggle = mask ^ (1 << bit), lowest = mask & -mask;
    int withoutLowest = mask & (mask - 1);
    int count = Integer.bitCount(mask), logicalShift = mask >>> 1;
    boolean powerOfTwo = mask > 0 && (mask & (mask - 1)) == 0;
    long wideBit = 1L << 40;
    // Java masks shift distances: 1 << 32 equals 1 << 0.
}
```

<a id="snippet-08"></a>

## 08. Node definitions

**Priority: Essential.**

```java
static class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}
static class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode(int val) { this.val = val; }
}
static class GraphNode {
    int val;
    List<GraphNode> neighbors = new ArrayList<>();
    GraphNode(int val) { this.val = val; }
}
```

<a id="snippet-09"></a>

## 09. Linked-list reverse cycle and merge

**Priority: Essential.**

```java
static ListNode reverseList(ListNode head) { // mutates links; O(n), O(1)
    ListNode previous = null;
    while (head != null) {
        ListNode next = head.next;
        head.next = previous;
        previous = head;
        head = next;
    }
    return previous;
}
static boolean hasCycle(ListNode head) { // O(n), O(1)
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}
static ListNode mergeLists(ListNode a, ListNode b) {
    // Sorted ascending, acyclic, disjoint lists; reuses and mutates nodes.
    ListNode dummy = new ListNode(0), tail = dummy;
    while (a != null && b != null) {
        if (a.val <= b.val) { tail.next = a; a = a.next; }
        else { tail.next = b; b = b.next; }
        tail = tail.next;
    }
    tail.next = a != null ? a : b;
    return dummy.next; // O(n+m), O(1) auxiliary space
}
```

<a id="snippet-10"></a>

## 10. Binary-search boundaries

**Priority: Essential.**

```java
static int lowerBound(int[] a, int target) {
    int left = 0, right = a.length; // search [left, right)
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (a[mid] < target) left = mid + 1;
        else right = mid;
    }
    return left; // first >= target; n if none
}
static int upperBound(int[] a, int target) {
    int left = 0, right = a.length;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (a[mid] <= target) left = mid + 1;
        else right = mid;
    }
    return left; // first > target; n if none
}
// Sorted ascending input. O(log n), O(1).
// count(target) = upperBound(a,target) - lowerBound(a,target).
// Exact match: int i = lowerBound(a,t); boolean found = i < a.length && a[i] == t;
```

<a id="snippet-11"></a>

## 11. Binary search on the answer

**Priority: Essential.**

```java
static int minEatingSpeed(int[] piles, long hours) {
    // Positive piles; one pile per hour, unused capacity cannot transfer.
    if (piles.length == 0) return 0;
    if (hours < piles.length) return -1;
    int left = 1, right = 0;
    for (int pile : piles) right = Math.max(right, pile);
    while (left < right) {
        int speed = left + (right - left) / 2;
        long needed = 0;
        for (int pile : piles) needed += ((long) pile + speed - 1) / speed;
        if (needed <= hours) right = speed; // feasible: seek smaller
        else left = speed + 1;
    }
    return left; // O(n log maxPile), O(1)
}
// Maximize feasible x: if (feasible(mid)) left = mid; else right = mid - 1;
// MUST use mid = left + (right - left + 1) / 2 when assigning left = mid,
// otherwise left == mid forever when right == left + 1.
```

<a id="snippet-12"></a>

## 12. Prefix sums and subarray-sum counting

**Priority: Essential.**

```java
static long[] prefixSums(int[] a) {
    long[] prefix = new long[a.length + 1];
    for (int i = 0; i < a.length; i++) prefix[i + 1] = prefix[i] + a[i];
    return prefix; // sum of [left,right) = prefix[right] - prefix[left]
}
static long subarraySumCount(int[] a, long target) {
    // Supports negative values; count can exceed int range.
    Map<Long, Long> frequencies = new HashMap<>();
    frequencies.put(0L, 1L);
    long prefix = 0, answer = 0;
    for (int x : a) {
        prefix += x;
        answer += frequencies.getOrDefault(prefix - target, 0L);
        frequencies.put(prefix, frequencies.getOrDefault(prefix, 0L) + 1);
    }
    return answer; // expected O(n) time, O(n) space
}
```

<a id="snippet-13"></a>

## 13. Two pointers on sorted input

**Priority: Essential.**

```java
static int[] twoSumSorted(int[] a, long target) {
    int left = 0, right = a.length - 1;
    while (left < right) {
        long sum = (long) a[left] + a[right];
        if (sum == target) return new int[]{left, right};
        if (sum < target) left++;
        else right--;
    }
    return new int[]{-1, -1}; // O(n), O(1); returns zero-based indices
}
```

<a id="snippet-14"></a>

## 14. Variable sliding window

**Priority: Essential.**

```java
static int longestAtMostKDistinct(String s, int k) {
    if (k <= 0) return 0;
    Map<Character, Integer> freq = new HashMap<>();
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        freq.put(c, freq.getOrDefault(c, 0) + 1);
        while (freq.size() > k) {
            char old = s.charAt(left++);
            int remaining = freq.get(old) - 1;
            if (remaining == 0) freq.remove(old);
            else freq.put(old, remaining);
        }
        best = Math.max(best, right - left + 1);
    }
    return best; // expected O(n); O(min(alphabet,k+1)) space; UTF-16 units
}
```

<a id="snippet-15"></a>

## 15. Fixed sliding window

**Priority: Essential.**

```java
static long maxWindowSum(int[] a, int k) {
    if (k < 1 || k > a.length) throw new IllegalArgumentException("k");
    long window = 0, best = Long.MIN_VALUE;
    for (int right = 0; right < a.length; right++) {
        window += a[right];
        if (right >= k) window -= a[right - k];
        if (right >= k - 1) best = Math.max(best, window);
    }
    return best; // O(n), O(1); works with all-negative arrays
}
```

<a id="snippet-16"></a>

## 16. Monotonic stack

**Priority: Essential.**

```java
static int[] nextGreaterIndex(int[] a) {
    int[] answer = new int[a.length];
    Arrays.fill(answer, -1);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < a.length; i++) {
        while (!stack.isEmpty() && a[stack.peek()] < a[i]) {
            answer[stack.pop()] = i;
        }
        stack.push(i);
    }
    return answer; // O(n), O(n); strictly greater, not greater-or-equal
}
```

<a id="snippet-17"></a>

## 17. Monotonic deque for sliding maximum

**Priority: Important.**

```java
static int[] slidingMaximum(int[] a, int k) {
    if (k < 1 || k > a.length) throw new IllegalArgumentException("k");
    int[] answer = new int[a.length - k + 1];
    Deque<Integer> deque = new ArrayDeque<>(); // indices, descending values
    for (int i = 0; i < a.length; i++) {
        while (!deque.isEmpty() && deque.peekFirst() <= i - k) deque.pollFirst();
        while (!deque.isEmpty() && a[deque.peekLast()] <= a[i]) deque.pollLast();
        deque.offerLast(i);
        if (i >= k - 1) answer[i - k + 1] = a[deque.peekFirst()];
    }
    return answer; // O(n), O(k) auxiliary space, excluding output
}
```

<a id="snippet-18"></a>

## 18. Merge intervals

**Priority: Essential.**

```java
static int[][] mergeIntervals(int[][] intervals) {
    // Closed intervals [start,end], start <= end; touching intervals merge.
    int[][] sorted = new int[intervals.length][];
    for (int i = 0; i < intervals.length; i++) sorted[i] = intervals[i].clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
    List<int[]> result = new ArrayList<>();
    for (int[] current : sorted) {
        if (result.isEmpty() || result.get(result.size() - 1)[1] < current[0]) {
            result.add(current);
        } else {
            int[] last = result.get(result.size() - 1);
            last[1] = Math.max(last[1], current[1]);
        }
    }
    return result.toArray(new int[0][]); // O(n log n), O(n); preserves input
}
```

<a id="snippet-19"></a>

## 19. Meeting rooms and endpoint semantics

**Priority: Important.**

```java
static int meetingRooms(int[][] intervals) {
    // Half-open [start,end), start < end. End at t frees the room for a start at t
    // (peek() <= start). Touching meetings share a room; they do not need two.
    int[][] sorted = intervals.clone(); // sorting outer array only; rows unchanged
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
    PriorityQueue<Integer> ends = new PriorityQueue<>();
    int best = 0;
    for (int[] interval : sorted) {
        while (!ends.isEmpty() && ends.peek() <= interval[0]) ends.poll();
        ends.offer(interval[1]);
        best = Math.max(best, ends.size());
    }
    return best; // O(n log n), O(n)
}
```

<a id="snippet-20"></a>

## 20. Tree inorder and level-order traversal

**Priority: Essential.**

```java
static List<Integer> inorder(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    Deque<TreeNode> stack = new ArrayDeque<>();
    TreeNode current = root;
    while (current != null || !stack.isEmpty()) {
        while (current != null) { stack.push(current); current = current.left; }
        current = stack.pop();
        result.add(current.val);
        current = current.right;
    }
    return result; // O(n), O(h) auxiliary space
}
static List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new ArrayDeque<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        int size = queue.size(); // snapshot before adding children
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            level.add(node.val);
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(level);
    }
    return result; // O(n), O(maximum width) auxiliary space
}
```

<a id="snippet-21"></a>

## 21. Tree recursion balance and LCA

**Priority: Essential.**

```java
static int heightOrUnbalanced(TreeNode root) {
    if (root == null) return 0;
    int left = heightOrUnbalanced(root.left);
    if (left == -1) return -1;
    int right = heightOrUnbalanced(root.right);
    if (right == -1 || Math.abs(left - right) > 1) return -1;
    return 1 + Math.max(left, right); // -1 means unbalanced
}
static TreeNode lca(TreeNode root, TreeNode p, TreeNode q) {
    // General binary tree; BOTH node references must exist in the tree.
    if (root == null || root == p || root == q) return root;
    TreeNode left = lca(root.left, p, q), right = lca(root.right, p, q);
    if (left != null && right != null) return root;
    return left != null ? left : right;
}
// Each O(n) time, O(h) call stack. Skewed trees can overflow Java's stack.
```

<a id="snippet-22"></a>

## 22. Validate a BST with bounds

**Priority: Essential.**

```java
static boolean validBST(TreeNode root) {
    return validBST(root, Long.MIN_VALUE, Long.MAX_VALUE);
}
static boolean validBST(TreeNode node, long low, long high) {
    if (node == null) return true;
    if (node.val <= low || node.val >= high) return false;
    return validBST(node.left, low, node.val) && validBST(node.right, node.val, high);
}
// Strict BST: duplicates disallowed. O(n), O(h). Long bounds admit all int values.
```

<a id="snippet-23"></a>

## 23. Graph construction DFS and BFS distances

**Priority: Essential.**

```java
static List<List<Integer>> graph(int n, int[][] edges, boolean directed) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    for (int[] edge : edges) {
        graph.get(edge[0]).add(edge[1]);
        if (!directed) graph.get(edge[1]).add(edge[0]);
    }
    return graph; // vertex IDs 0..n-1
}
static int[] bfsDistances(List<List<Integer>> graph, int source) {
    int[] distance = new int[graph.size()];
    Arrays.fill(distance, -1);
    Queue<Integer> queue = new ArrayDeque<>();
    distance[source] = 0;
    queue.offer(source);
    while (!queue.isEmpty()) {
        int u = queue.poll();
        for (int v : graph.get(u)) {
            if (distance[v] != -1) continue;
            distance[v] = distance[u] + 1; // mark when enqueuing
            queue.offer(v);
        }
    }
    return distance; // unweighted shortest paths; -1 means unreachable
}
static int connectedComponents(List<List<Integer>> graph) {
    // UNDIRECTED graph. This is not an SCC algorithm for directed graphs.
    boolean[] visited = new boolean[graph.size()];
    int components = 0;
    Deque<Integer> stack = new ArrayDeque<>();
    for (int start = 0; start < graph.size(); start++) {
        if (visited[start]) continue;
        components++;
        visited[start] = true;
        stack.push(start);
        while (!stack.isEmpty()) {
            int u = stack.pop();
            for (int v : graph.get(u)) {
                if (!visited[v]) { visited[v] = true; stack.push(v); }
            }
        }
    }
    return components;
}
// Each traversal O(V+E) time, O(V) auxiliary space (excluding adjacency).
```

<a id="snippet-24"></a>

## 24. Grid and multi-source BFS

**Priority: Essential.**

```java
static int[][] distanceToZero(int[][] grid) {
    // Rectangular binary grid; all cells traversable. No zero => all -1.
    int rows = grid.length, cols = rows == 0 ? 0 : grid[0].length;
    int[][] dist = new int[rows][cols];
    Queue<int[]> queue = new ArrayDeque<>();
    for (int r = 0; r < rows; r++) {
        Arrays.fill(dist[r], -1);
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == 0) { dist[r][c] = 0; queue.offer(new int[]{r, c}); }
        }
    }
    int[][] directions = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    while (!queue.isEmpty()) {
        int[] cell = queue.poll();
        for (int[] d : directions) {
            int r = cell[0] + d[0], c = cell[1] + d[1];
            if (r < 0 || r >= rows || c < 0 || c >= cols || dist[r][c] != -1) continue;
            dist[r][c] = dist[cell[0]][cell[1]] + 1;
            queue.offer(new int[]{r, c});
        }
    }
    return dist; // O(rows*cols) time and space; input unchanged
}
```

<a id="snippet-25"></a>

## 25. Topological sort and directed cycle detection

**Priority: Essential.**

```java
static int[] topologicalSort(List<List<Integer>> graph) {
    int n = graph.size();
    int[] indegree = new int[n], order = new int[n];
    for (List<Integer> neighbors : graph) for (int v : neighbors) indegree[v]++;
    Queue<Integer> queue = new ArrayDeque<>();
    for (int u = 0; u < n; u++) if (indegree[u] == 0) queue.offer(u);
    int count = 0;
    while (!queue.isEmpty()) {
        int u = queue.poll();
        order[count++] = u;
        for (int v : graph.get(u)) if (--indegree[v] == 0) queue.offer(v);
    }
    return count == n ? order : new int[0];
    // Nonempty graph + empty result => cycle. Empty graph has valid empty order.
    // Edge u->v means u must precede v. O(V+E), O(V) auxiliary space.
}
```

<a id="snippet-26"></a>

## 26. Dijkstra with stale-entry skipping

**Priority: Essential.**

```java
static class Edge {
    final int to, weight;
    Edge(int to, int weight) { this.to = to; this.weight = weight; }
}
static long[] dijkstra(List<List<Edge>> graph, int source) {
    // All weights >= 0; finite distances fit in long and are < Long.MAX_VALUE.
    long[] dist = new long[graph.size()];
    Arrays.fill(dist, Long.MAX_VALUE);
    PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    dist[source] = 0;
    heap.offer(new long[]{0, source}); // {distance, node}
    while (!heap.isEmpty()) {
        long[] current = heap.poll();
        long distance = current[0];
        int u = (int) current[1];
        if (distance != dist[u]) continue;
        for (Edge edge : graph.get(u)) {
            long candidate = distance + edge.weight;
            if (candidate < dist[edge.to]) {
                dist[edge.to] = candidate;
                heap.offer(new long[]{candidate, edge.to});
            }
        }
    }
    return dist; // Long.MAX_VALUE means unreachable.
    // Lazy heap: O(V + E log(E+1)) time, O(V+E) auxiliary space.
}
```

<a id="snippet-27"></a>

## 27. Union-find with size and path compression

**Priority: Essential.**

```java
static class UnionFind {
    final int[] parent, size;
    int components;
    UnionFind(int n) {
        parent = new int[n]; size = new int[n]; components = n;
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
    }
    int find(int x) {
        while (x != parent[x]) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }
    boolean union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;
        if (size[ra] < size[rb]) { int temp = ra; ra = rb; rb = temp; }
        parent[rb] = ra;
        size[ra] += size[rb];
        components--;
        return true;
    }
}
// Amortized O(alpha(n)) per operation, O(n) storage, O(n) initialization.
// union returning false detects a redundant edge in an undirected graph.
```

<a id="snippet-28"></a>

## 28. Trie insert search and prefix

**Priority: Essential.**

```java
static class Trie {
    static class Node { Node[] next = new Node[26]; boolean word; }
    final Node root = new Node();
    void insert(String s) { // lowercase a-z only; supports empty word
        Node node = root;
        for (int i = 0; i < s.length(); i++) {
            int index = s.charAt(i) - 'a';
            if (node.next[index] == null) node.next[index] = new Node();
            node = node.next[index];
        }
        node.word = true;
    }
    Node walk(String s) {
        Node node = root;
        for (int i = 0; i < s.length(); i++) {
            node = node.next[s.charAt(i) - 'a'];
            if (node == null) return null;
        }
        return node;
    }
    boolean search(String s) { Node node = walk(s); return node != null && node.word; }
    boolean startsWith(String prefix) { return walk(prefix) != null; }
}
// O(length) per operation; space proportional to total inserted characters
// with 26 child slots per node. Use a map for a sparse/larger alphabet.
```

<a id="snippet-29"></a>

## 29. Backtracking subsets and unique permutations

**Priority: Essential.**

```java
static List<List<Integer>> subsets(int[] a) { // assumes distinct input values
    List<List<Integer>> result = new ArrayList<>();
    subsets(a, 0, new ArrayList<>(), result);
    return result;
}
static void subsets(int[] a, int start, List<Integer> path, List<List<Integer>> result) {
    result.add(new ArrayList<>(path)); // copy, never add the mutable path itself
    for (int i = start; i < a.length; i++) {
        path.add(a[i]);
        subsets(a, i + 1, path, result);
        path.remove(path.size() - 1);
    }
}
static List<List<Integer>> uniquePermutations(int[] input) {
    int[] a = input.clone(); Arrays.sort(a);
    List<List<Integer>> result = new ArrayList<>();
    permute(a, new boolean[a.length], new ArrayList<>(), result);
    return result;
}
static void permute(int[] a, boolean[] used, List<Integer> path, List<List<Integer>> result) {
    if (path.size() == a.length) { result.add(new ArrayList<>(path)); return; }
    for (int i = 0; i < a.length; i++) {
        if (used[i] || (i > 0 && a[i] == a[i - 1] && !used[i - 1])) continue;
        used[i] = true; path.add(a[i]);
        permute(a, used, path, result);
        path.remove(path.size() - 1); used[i] = false;
    }
}
// Subsets O(n*2^n); permutations O(n*n!) worst case, including output copies.
// O(n) auxiliary space excluding returned output. Empty input yields [[]].
```

<a id="snippet-30"></a>

## 30. Bottom-up DP coin change

**Priority: Essential.**

```java
static int coinChange(int[] coins, int amount) {
    // Positive coin values, unlimited reuse, 0 <= amount < Integer.MAX_VALUE;
    // amount must be small enough to allocate the DP array.
    int impossible = amount + 1;
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, impossible); dp[0] = 0;
    for (int value = 1; value <= amount; value++) {
        for (int coin : coins) {
            if (coin <= value && dp[value - coin] != impossible)
                dp[value] = Math.min(dp[value], dp[value - coin] + 1);
        }
    }
    return dp[amount] == impossible ? -1 : dp[amount];
    // dp[value] = minimum coins for exactly value. O(amount*coins), O(amount).
    // 0/1 knapsack compresses capacity DESCENDING to prevent item reuse.
}
```

<a id="snippet-31"></a>

## 31. Two-dimensional DP longest common subsequence

**Priority: Essential.**

```java
static int lcs(String a, String b) {
    int[][] dp = new int[a.length() + 1][b.length() + 1];
    for (int i = 1; i <= a.length(); i++) {
        for (int j = 1; j <= b.length(); j++) {
            if (a.charAt(i - 1) == b.charAt(j - 1)) dp[i][j] = 1 + dp[i - 1][j - 1];
            else dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
        }
    }
    return dp[a.length()][b.length()]; // O(m*n) time and space
    // dp[i][j] refers to prefixes of lengths i and j, not character indices.
}
```

<a id="snippet-32"></a>

## 32. Top-down memoization

**Priority: Essential.**

```java
static long minPathSum(int[][] grid) {
    // Nonempty rectangular grid, move only right/down; negative costs allowed.
    return minPathSum(grid, 0, 0, new Long[grid.length][grid[0].length]);
}
static long minPathSum(int[][] g, int r, int c, Long[][] memo) {
    if (memo[r][c] != null) return memo[r][c];
    if (r == g.length - 1 && c == g[0].length - 1) return memo[r][c] = (long) g[r][c];
    long best = Long.MAX_VALUE;
    if (r + 1 < g.length) best = Math.min(best, minPathSum(g, r + 1, c, memo));
    if (c + 1 < g[0].length) best = Math.min(best, minPathSum(g, r, c + 1, memo));
    return memo[r][c] = g[r][c] + best;
}
// O(rows*cols) time/memo storage; O(rows+cols) recursion depth.
// null means uncomputed: -1 is unsafe as a sentinel when valid results include -1.
```

<a id="snippet-33"></a>

## 33. Longest increasing subsequence

**Priority: Important.**

```java
static int lisLength(int[] a) {
    int[] tails = new int[a.length];
    int size = 0;
    for (int x : a) {
        int left = 0, right = size;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (tails[mid] < x) left = mid + 1;
            else right = mid;
        }
        tails[left] = x;
        if (left == size) size++;
    }
    return size; // strictly increasing; O(n log n), O(n)
    // tails[i] is the smallest known tail for length i+1; NOT the actual LIS.
}
```

<a id="snippet-34"></a>

## 34. Merge sort

**Priority: Important.**

```java
static void mergeSort(int[] a) { mergeSort(a, new int[a.length], 0, a.length); }
static void mergeSort(int[] a, int[] temp, int left, int right) {
    if (right - left <= 1) return;
    int mid = left + (right - left) / 2;
    mergeSort(a, temp, left, mid); mergeSort(a, temp, mid, right);
    int i = left, j = mid, write = left;
    while (i < mid && j < right) temp[write++] = a[i] <= a[j] ? a[i++] : a[j++];
    while (i < mid) temp[write++] = a[i++];
    while (j < right) temp[write++] = a[j++];
    for (int k = left; k < right; k++) a[k] = temp[k];
}
// [left,right); stable; mutates input. O(n log n), O(n) auxiliary space.
```

<a id="snippet-35"></a>

## 35. Randomized three-way quickselect

**Priority: Stretch.**

```java
static int kthSmallest(int[] a, int k) {
    // 1-based k; MUTATES input. Three-way partition handles duplicate pivots.
    if (k < 1 || k > a.length) throw new IllegalArgumentException("k");
    Random random = new Random();
    int target = k - 1, left = 0, right = a.length - 1;
    while (left <= right) {
        int pivot = a[left + random.nextInt(right - left + 1)];
        int less = left, scan = left, greater = right;
        while (scan <= greater) {
            if (a[scan] < pivot) swap(a, less++, scan++);
            else if (a[scan] > pivot) swap(a, scan, greater--);
            else scan++;
        }
        if (target < less) right = less - 1;
        else if (target > greater) left = greater + 1;
        else return pivot;
    }
    throw new AssertionError("unreachable");
}
static void swap(int[] a, int i, int j) { int temp = a[i]; a[i] = a[j]; a[j] = temp; }
// Expected O(n), worst O(n^2), O(1) auxiliary space.
```

<a id="snippet-36"></a>

## 36. Fenwick tree for point updates and range sums

**Priority: Stretch.**

```java
static class Fenwick {
    final long[] tree;
    Fenwick(int n) { tree = new long[n + 1]; }
    void add(int index, long delta) { // external zero-based index
        if (index < 0 || index >= tree.length - 1) throw new IndexOutOfBoundsException();
        for (int i = index + 1; i < tree.length; i += i & -i) tree[i] += delta;
    }
    long prefix(int end) { // sum of [0,end)
        if (end < 0 || end >= tree.length) throw new IndexOutOfBoundsException();
        long sum = 0;
        for (int i = end; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    }
    long range(int left, int right) { return prefix(right) - prefix(left); }
}
// O(log n) per add/query, O(n) storage. Valid range: 0 <= left <= right <= n.
```

<a id="snippet-37"></a>

## 37. LRU cache using library primitives

**Priority: Important.**

```java
static class LruCache {
    final int capacity;
    final LinkedHashMap<Integer, Integer> map = new LinkedHashMap<>(16, 0.75f, true);
    LruCache(int capacity) {
        if (capacity < 0) throw new IllegalArgumentException("capacity");
        this.capacity = capacity;
    }
    Integer get(int key) { return map.get(key); } // null if absent; refreshes recency
    void put(int key, int value) {
        map.put(key, value);
        if (map.size() > capacity) {
            Iterator<Integer> iterator = map.keySet().iterator();
            iterator.next(); iterator.remove(); // least recently accessed
        }
    }
}
// Expected O(1) get/put, O(capacity) storage; not thread-safe.
// If asked to implement internals, explain/map out hash map + doubly linked list.
```

<a id="snippet-38"></a>

## 38. Immutable composite hash-map key

**Priority: Important.**

```java
static final class Cell {
    final int row, col;
    Cell(int row, int col) { this.row = row; this.col = col; }
    @Override public boolean equals(Object other) {
        if (this == other) return true;
        if (!(other instanceof Cell)) return false;
        Cell cell = (Cell) other;
        return row == cell.row && col == cell.col;
    }
    @Override public int hashCode() { return 31 * row + col; }
}
// Set<Cell> cells = new HashSet<>(); cells.add(new Cell(1,2));
// cells.contains(new Cell(1,2)) is true. int[] keys instead use identity equality.
// Hash collisions are allowed; equal objects MUST have equal hash codes.
```

<a id="snippet-39"></a>

## 39. Kadane maximum subarray

**Priority: Essential.**

```java
static long maxSubarray(int[] a) {
    if (a.length == 0) throw new IllegalArgumentException("nonempty array required");
    long endingHere = a[0], best = a[0];
    for (int i = 1; i < a.length; i++) {
        endingHere = Math.max((long) a[i], endingHere + a[i]);
        best = Math.max(best, endingHere);
    }
    return best; // nonempty subarray; O(n), O(1); handles all-negative input
}
```

<a id="snippet-40"></a>

## 40. One-dimensional 0-1 knapsack

**Priority: Important.**

```java
static long knapsack(int[] weights, int[] values, int capacity) {
    // Same-length arrays; weights > 0; capacity >= 0; choosing no items allowed.
    long[] dp = new long[capacity + 1];
    for (int i = 0; i < weights.length; i++) {
        for (int room = capacity; room >= weights[i]; room--) {
            dp[room] = Math.max(dp[room], dp[room - weights[i]] + values[i]);
        }
    }
    return dp[capacity]; // O(items*capacity), O(capacity)
    // Descending room prevents reusing this item; ascending would allow reuse.
}
```

<a id="snippet-41"></a>

## 41. LRU internals hash map and doubly linked list

**Priority: Important.**

```java
static class ManualLruCache {
    static class Node {
        final int key;
        int value;
        Node prev, next;
        Node(int key, int value) { this.key = key; this.value = value; }
    }
    final int capacity;
    final Map<Integer, Node> map = new HashMap<>();
    final Node head = new Node(0, 0), tail = new Node(0, 0);
    ManualLruCache(int capacity) {
        if (capacity < 0) throw new IllegalArgumentException("capacity");
        this.capacity = capacity;
        head.next = tail; tail.prev = head;
    }
    void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    void addMostRecent(Node node) { // insert immediately after head sentinel
        node.prev = head; node.next = head.next;
        head.next.prev = node; head.next = node;
    }
    Integer get(int key) {
        Node node = map.get(key);
        if (node == null) return null;
        unlink(node); addMostRecent(node);
        return node.value;
    }
    void put(int key, int value) {
        Node node = map.get(key);
        if (node != null) { node.value = value; unlink(node); }
        else { node = new Node(key, value); map.put(key, node); }
        addMostRecent(node);
        if (map.size() > capacity) {
            Node victim = tail.prev;
            unlink(victim); map.remove(victim.key);
        }
    }
}
// Expected O(1) per get/put, O(capacity) space; zero capacity works.
// Invariant: every map node appears once between head and tail; most recent first.
```

<a id="snippet-42"></a>

## 42. Bipartite graph coloring

**Priority: Important.**

```java
static boolean isBipartite(List<List<Integer>> graph) {
    // Undirected graph; handles disconnected components and self-loops.
    int[] color = new int[graph.size()]; // 0 unvisited, +1/-1 colors
    Queue<Integer> queue = new ArrayDeque<>();
    for (int start = 0; start < graph.size(); start++) {
        if (color[start] != 0) continue;
        color[start] = 1; queue.offer(start);
        while (!queue.isEmpty()) {
            int u = queue.poll();
            for (int v : graph.get(u)) {
                if (color[v] == color[u]) return false;
                if (color[v] == 0) { color[v] = -color[u]; queue.offer(v); }
            }
        }
    }
    return true; // O(V+E) time, O(V) auxiliary space
}
```

<a id="snippet-43"></a>

## 43. Linked-list dummy, middle, reverse-k

**Priority: Essential.**

```java
static ListNode removeNthFromEnd(ListNode head, int n) {
    // Acyclic list; 1 <= n <= length. Mutates links. Reject invalid n.
    if (n < 1) throw new IllegalArgumentException("n must be positive");
    ListNode dummy = new ListNode(0);
    dummy.next = head;
    ListNode fast = dummy, slow = dummy;
    for (int i = 0; i < n; i++) {
        if (fast.next == null) throw new IllegalArgumentException("n exceeds length");
        fast = fast.next;
    }
    while (fast.next != null) { fast = fast.next; slow = slow.next; }
    slow.next = slow.next.next;
    return dummy.next; // O(L), O(1)
}
static ListNode middleNode(ListNode head) {
    // Acyclic list; null input returns null; does not mutate links.
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow; // second middle on even length; O(L), O(1)
}
static ListNode reverseKGroup(ListNode head, int k) {
    // Acyclic list; k >= 1. Mutates links; incomplete final group is unchanged.
    if (k < 1) throw new IllegalArgumentException("k must be positive");
    ListNode dummy = new ListNode(0);
    dummy.next = head;
    ListNode groupPrev = dummy;
    while (true) {
        ListNode kth = groupPrev;
        for (int i = 0; i < k && kth != null; i++) kth = kth.next;
        if (kth == null) break;
        ListNode groupNext = kth.next;
        ListNode prev = groupNext, cur = groupPrev.next;
        while (cur != groupNext) {
            ListNode nxt = cur.next;
            cur.next = prev;
            prev = cur;
            cur = nxt;
        }
        ListNode newEnd = groupPrev.next;
        groupPrev.next = kth;
        groupPrev = newEnd;
    }
    return dummy.next; // O(L), O(1)
}
```

<a id="snippet-44"></a>

## 44. Minimum covering window

**Priority: Essential.**

```java
static String minWindow(String s, String t) {
    // Smallest substring of s covering every character of t (counts matter).
    // ASCII. Empty t or |s| < |t| => "".
    if (t.isEmpty() || s.length() < t.length()) return "";
    int[] need = new int[128], window = new int[128];
    int required = 0;
    for (int i = 0; i < t.length(); i++) if (need[t.charAt(i)]++ == 0) required++;
    int formed = 0, left = 0, bestLen = Integer.MAX_VALUE, bestL = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        if (++window[c] == need[c] && need[c] > 0) formed++;
        while (formed == required) {
            if (right - left + 1 < bestLen) {
                bestLen = right - left + 1;
                bestL = left;
            }
            char old = s.charAt(left++);
            window[old]--; // keep counts accurate even for characters absent from t
            if (need[old] > 0 && window[old] < need[old]) formed--;
        }
    }
    return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestL, bestL + bestLen);
    // O(|s|+|t|), O(1) extra for ASCII. Track satisfied unique chars, not raw totals.
}
```

<a id="snippet-45"></a>

## 45. 2D prefix sums and difference array

**Priority: Important.**

```java
static long[][] prefix2D(int[][] a) {
    // Rectangular input; arithmetic and intermediate sums must fit in long.
    int rows = a.length, cols = rows == 0 ? 0 : a[0].length;
    long[][] p = new long[rows + 1][cols + 1];
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            p[i + 1][j + 1] = a[i][j] + p[i][j + 1] + p[i + 1][j] - p[i][j];
        }
    }
    return p; // Build time/space O((rows+1)*(cols+1)); rectangle queries are O(1).
    // Inclusive rectangle: p[r2+1][c2+1]-p[r1][c2+1]-p[r2+1][c1]+p[r1][c1].
}
static void rangeAdd(long[] diff, int left, int right, long val) {
    // Inclusive [left,right]; diff.length == n+1; 0 <= left <= right < n.
    // Start with a zeroed diff array; all update arithmetic must fit in long.
    if (left < 0 || left > right || right >= diff.length - 1)
        throw new IllegalArgumentException("invalid range");
    diff[left] += val;
    diff[right + 1] -= val; // sentinel is always allocated; O(1) update
}
static long[] materialize(long[] diff, int n) {
    // Produces accumulated increments to an initially zero array, not an existing base.
    if (n < 0 || n != diff.length - 1) throw new IllegalArgumentException("invalid n");
    long[] a = new long[n];
    long cur = 0;
    for (int i = 0; i < n; i++) { cur += diff[i]; a[i] = cur; }
    return a; // O(n) time/output space, O(1) auxiliary space beyond output
}
```

<a id="snippet-46"></a>

## 46. 0-1 BFS

**Priority: Important.**

```java
static int[] zeroOneBfs(List<List<int[]>> graph, int source) {
    // Vertex IDs 0..n-1; valid source; entries {to, weight}, weight in {0,1}.
    // O(V+E) time; a specialized alternative to Dijkstra, which also works here.
    int n = graph.size();
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    Deque<Integer> deque = new ArrayDeque<>();
    dist[source] = 0;
    deque.offer(source);
    while (!deque.isEmpty()) {
        int u = deque.pollFirst();
        for (int[] edge : graph.get(u)) {
            int v = edge[0], w = edge[1], nd = dist[u] + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                if (w == 0) deque.offerFirst(v);
                else deque.offerLast(v);
            }
        }
    }
    return dist; // Integer.MAX_VALUE means unreachable; O(V+E) space upper bound
}
```

<a id="snippet-47"></a>

## 47. Grid DFS islands

**Priority: Essential.**

```java
static int numIslands(char[][] grid) {
    // Rectangular '0'/'1' grid, 4-neighbor; mutates '1' -> '0'.
    // Iterative to avoid StackOverflowError on snakes; copy input to preserve it.
    if (grid.length == 0) return 0;
    int rows = grid.length, cols = grid[0].length, count = 0;
    int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    Deque<int[]> stack = new ArrayDeque<>();
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] != '1') continue;
            count++;
            grid[r][c] = '0';
            stack.push(new int[]{r, c});
            while (!stack.isEmpty()) {
                int[] cell = stack.pop();
                for (int[] d : dirs) {
                    int nr = cell[0] + d[0], nc = cell[1] + d[1];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] != '1') continue;
                    grid[nr][nc] = '0'; // mark when pushing
                    stack.push(new int[]{nr, nc});
                }
            }
        }
    }
    return count; // O(rows*cols) time and worst-case stack space
}
```

<a id="snippet-48"></a>

## 48. Serialize and deserialize a binary tree

**Priority: Important.**

```java
static String serialize(TreeNode root) {
    // Integer-valued binary tree; null encodes as "#".
    StringBuilder sb = new StringBuilder();
    serializeDfs(root, sb);
    return sb.toString();
}
static void serializeDfs(TreeNode node, StringBuilder sb) {
    if (sb.length() > 0) sb.append(',');
    if (node == null) { sb.append('#'); return; }
    sb.append(node.val);
    serializeDfs(node.left, sb);
    serializeDfs(node.right, sb);
}
static TreeNode deserialize(String data) {
    // Requires valid output of serialize; this is not a malformed-input validator.
    return deserializeDfs(new ArrayDeque<String>(Arrays.asList(data.split(",", -1))));
}
static TreeNode deserializeDfs(Queue<String> tokens) {
    String tok = tokens.poll();
    if ("#".equals(tok)) return null;
    TreeNode node = new TreeNode(Integer.parseInt(tok));
    node.left = deserializeDfs(tokens);
    node.right = deserializeDfs(tokens);
    return node;
}
// O(n) time for int-valued nodes; O(h) call stack, plus O(n) output/tokens.
// Recursive teaching template: deep skewed trees can overflow; use an explicit stack then.
```

<a id="snippet-49"></a>

## 49. Edit distance

**Priority: Important.**

```java
static int editDistance(String a, String b) {
    // Unit-cost insert/delete/replace; compares UTF-16 code units, not grapheme clusters.
    int m = a.length(), n = b.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 0; i <= m; i++) dp[i][0] = i; // delete all
    for (int j = 0; j <= n; j++) dp[0][j] = j; // insert all
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (a.charAt(i - 1) == b.charAt(j - 1)) dp[i][j] = dp[i - 1][j - 1];
            else dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1]));
        }
    }
    return dp[m][n]; // O((m+1)*(n+1)) time and space, including empty-string boundaries
}
```

<a id="snippet-50"></a>

## 50. Decode string

**Priority: Important.**

```java
static String decodeString(String s) {
    // Well-formed encoding: ASCII letters and positive count[content] groups.
    // Counts must fit int; decoded strings must fit Java String size and available memory.
    // Empty input/content is supported. Digits occur only as repeat counts.
    Deque<Integer> counts = new ArrayDeque<>();
    Deque<StringBuilder> frames = new ArrayDeque<>();
    StringBuilder cur = new StringBuilder();
    int num = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c >= '0' && c <= '9') {
            int digit = c - '0';
            if (num > (Integer.MAX_VALUE - digit) / 10)
                throw new IllegalArgumentException("repeat count exceeds int range");
            num = num * 10 + digit;
        }
        else if (c == '[') {
            if (num < 1) throw new IllegalArgumentException("repeat count must be positive");
            counts.push(num);
            frames.push(cur);
            cur = new StringBuilder();
            num = 0;
        } else if (c == ']') {
            StringBuilder prev = frames.pop();
            int k = counts.pop();
            long expandedLength = prev.length() + (long) k * cur.length();
            if (expandedLength > Integer.MAX_VALUE)
                throw new IllegalArgumentException("decoded string exceeds Java length range");
            if (cur.length() > 0) { // avoid k iterations when content is empty
                for (int t = 0; t < k; t++) prev.append(cur);
            }
            cur = prev;
        } else cur.append(c);
    }
    return cur.toString();
}
// N = input length, L = decoded length, D = maximum nesting depth.
// Time O(N + (D+1)*L) upper bound: nested frames can copy the same output repeatedly.
// More precisely, count the sum of expansions at every closing bracket, plus input/output.
// Auxiliary space O(D+L), excluding input. The positive-count contract matters for this bound.
```

<a id="snippet-51"></a>

## 51. Merge k sorted lists

**Priority: Important.**

```java
static ListNode mergeKLists(ListNode[] lists) {
    // Non-null array of ascending, acyclic, pairwise-disjoint lists; null heads allowed.
    // Reuses nodes and mutates links; shared nodes between lists violate this contract.
    PriorityQueue<ListNode> heap = new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));
    for (ListNode node : lists) if (node != null) heap.offer(node);
    ListNode dummy = new ListNode(0), tail = dummy;
    while (!heap.isEmpty()) {
        ListNode node = heap.poll();
        tail.next = node;
        tail = node;
        if (node.next != null) heap.offer(node.next);
    }
    return dummy.next; // O(k + N log(k+1)) time, O(k) auxiliary; k lists, N total nodes
}
```

<a id="snippet-52"></a>

## 52. Directed cycle detection, DFS 3-color

**Priority: Important.**

```java
static boolean hasDirectedCycle(List<List<Integer>> graph) {
    // Vertex IDs 0..n-1; covers all components, self-loops, and duplicate edges.
    int n = graph.size();
    int[] color = new int[n]; // 0 unvisited, 1 on stack, 2 done
    for (int u = 0; u < n; u++) {
        if (color[u] == 0 && dfsCycle(graph, u, color)) return true;
    }
    return false;
}
static boolean dfsCycle(List<List<Integer>> graph, int u, int[] color) {
    color[u] = 1;
    for (int v : graph.get(u)) {
        if (color[v] == 1) return true;          // back edge
        if (color[v] == 0 && dfsCycle(graph, v, color)) return true;
    }
    color[u] = 2;
    return false;
}
// Gray (1) neighbor => cycle. Kahn (25) is usually enough; use this when you already DFS.
// Recursion depth O(V); deep chains can cause StackOverflowError.
// O(V+E) time, O(V) auxiliary. Use Kahn (25) or an explicit DFS stack for deep graphs.
```

<a id="snippet-53"></a>

## 53. Grid word search

**Priority: Important.**

```java
static boolean wordSearch(char[][] board, String word) {
    // Rectangular board; any char (including '#'); four-neighbor moves; no cell reuse.
    // This API treats an empty word as false. Leaves the board unchanged.
    if (board.length == 0 || board[0].length == 0 || word.isEmpty()) return false;
    if (word.length() > (long) board.length * board[0].length) return false;
    boolean[][] used = new boolean[board.length][board[0].length];
    for (int r = 0; r < board.length; r++) {
        for (int c = 0; c < board[0].length; c++) {
            if (wordDfs(board, word, 0, r, c, used)) return true;
        }
    }
    return false;
}
static boolean wordDfs(char[][] board, String word, int i, int r, int c, boolean[][] used) {
    if (r < 0 || r >= board.length || c < 0 || c >= board[0].length
            || used[r][c] || board[r][c] != word.charAt(i))
        return false;
    if (i == word.length() - 1) return true;
    used[r][c] = true;
    boolean found = wordDfs(board, word, i + 1, r + 1, c, used)
            || wordDfs(board, word, i + 1, r - 1, c, used)
            || wordDfs(board, word, i + 1, r, c + 1, used)
            || wordDfs(board, word, i + 1, r, c - 1, used);
    used[r][c] = false; // restore the path state on both success and failure
    return found;
}
// O(R*C*4^L) time upper bound; O(R*C + L) auxiliary space for visited + recursion.
// Large L can exceed the call-stack limit; choose an iterative search if required.
```

## A realistic final-week recall drill

Use the final week's coding allocation from the study plan rather than adding a second workload.

- **Session 1, 45 min:** collection syntax and comparators, lower/upper bound, prefix sums; check overflow and duplicate cases.
- **Session 2, 60 min:** BFS, topological sort, Dijkstra, union-find; explain algorithm selection and trace one graph.
- **Session 3, 45 min:** a variable window, tree postorder, and one DP recurrence; explain each invariant and base case.
- **Session 4, 60 min:** one unfamiliar 45-minute problem and a 15-minute debrief. Use templates only after deriving the model.
- **Final 30 min:** review your personal error log and the Java traps above. Skip new stretch algorithms.

For every snippet you practise, answer: **When is it valid? What invariant makes it correct? What mutates? What are time and auxiliary-space costs? Which edge case could break it?**
