import java.util.*;

/** Deterministic examples and randomized comparisons against small brute-force oracles. */
public class JavaInterviewTemplatesTest extends JavaInterviewTemplates {
    static int checks;
    static final Random RANDOM = new Random(20260907L);
    static void check(boolean condition, String label) {
        checks++;
        if (!condition) throw new AssertionError(label);
    }
    static void eq(long actual, long expected, String label) {
        check(actual == expected, label + ": expected " + expected + ", got " + actual);
    }
    static ListNode list(int... values) {
        ListNode dummy = new ListNode(0), tail = dummy;
        for (int value : values) { tail.next = new ListNode(value); tail = tail.next; }
        return dummy.next;
    }
    static List<Integer> values(ListNode head) {
        List<Integer> result = new ArrayList<>();
        while (head != null) { result.add(head.val); head = head.next; }
        return result;
    }
    static void examples() {
        arraysAndLists(); dequeTools(); comparatorTools(); orderedTools(); numericTools();
        check(stringTools("abcd").equals("cba"), "string tools");
        check(stringTools("").equals(""), "empty string");
        eq(frequencies(new int[]{1, 1, 2}).get(1), 2, "frequency");
        eq(gcd(48, 18), 6, "gcd"); eq(gcd(0, 0), 0, "zero gcd");
        eq(modPow(-2, 3, 5), 2, "negative modular base");
        eq(modPow(3, 0, 1), 0, "mod one");
        check(values(reverseList(list(1, 2, 3))).equals(Arrays.asList(3, 2, 1)), "reverse");
        check(reverseList(null) == null, "empty reverse");
        check(values(mergeLists(list(1, 3), list(2, 4))).equals(Arrays.asList(1, 2, 3, 4)), "merge lists");
        ListNode cycle = list(1, 2, 3); cycle.next.next.next = cycle.next;
        check(hasCycle(cycle) && !hasCycle(list(1)) && !hasCycle(null), "cycle");
        eq(minEatingSpeed(new int[]{3, 6, 7, 11}, 8), 4, "answer search");
        eq(minEatingSpeed(new int[]{1, 2}, 1), -1, "impossible hours");
        eq(minEatingSpeed(new int[]{Integer.MAX_VALUE}, Integer.MAX_VALUE), 1, "large hours");
        eq(subarraySumCount(new int[100000], 0), 5000050000L, "long subarray count");
        eq(maxSubarray(new int[]{Integer.MAX_VALUE, Integer.MAX_VALUE}), 4294967294L, "long sum");
        check(Arrays.deepEquals(mergeIntervals(new int[][]{{1, 3}, {3, 5}, {8, 9}}),
                new int[][]{{1, 5}, {8, 9}}), "closed endpoints");
        eq(mergeIntervals(new int[0][]).length, 0, "empty intervals");
        eq(meetingRooms(new int[][]{{1, 3}, {3, 5}}), 1, "half-open endpoints");
        TreeNode root = new TreeNode(2); root.left = new TreeNode(1); root.right = new TreeNode(3);
        check(inorder(root).equals(Arrays.asList(1, 2, 3)), "inorder");
        check(levelOrder(root).equals(Arrays.asList(Arrays.asList(2), Arrays.asList(1, 3))), "levels");
        eq(heightOrUnbalanced(root), 2, "balanced");
        check(lca(root, root.left, root.right) == root, "lca identity");
        check(validBST(root), "valid bst"); root.left.val = 2; check(!validBST(root), "duplicate bst");
        TreeNode extremes = new TreeNode(Integer.MIN_VALUE); extremes.right = new TreeNode(Integer.MAX_VALUE);
        check(validBST(extremes), "bst int extremes");
        extremes.right.right = new TreeNode(1); eq(heightOrUnbalanced(extremes), -1, "unbalanced");
        check(inorder(null).isEmpty() && levelOrder(null).isEmpty(), "empty trees");
        List<List<Integer>> g = graph(4, new int[][]{{0, 1}, {1, 2}}, false);
        check(Arrays.equals(bfsDistances(g, 0), new int[]{0, 1, 2, -1}), "bfs distances");
        eq(connectedComponents(g), 2, "components");
        check(isBipartite(g), "bipartite path");
        check(!isBipartite(graph(3, new int[][]{{0, 1}, {1, 2}, {2, 0}}, false)), "odd cycle");
        check(!isBipartite(graph(1, new int[][]{{0, 0}}, false)), "self loop");
        check(Arrays.deepEquals(distanceToZero(new int[][]{{0, 1, 1}, {1, 1, 0}}),
                new int[][]{{0, 1, 1}, {1, 1, 0}}), "multi source");
        check(Arrays.deepEquals(distanceToZero(new int[][]{{1, 1}}), new int[][]{{-1, -1}}), "no source");
        eq(distanceToZero(new int[0][]).length, 0, "empty grid");
        eq(topologicalSort(graph(2, new int[][]{{0, 1}, {1, 0}}, true)).length, 0, "topo cycle");
        Trie trie = new Trie(); trie.insert("apple"); trie.insert("");
        check(trie.search("apple") && !trie.search("app") && trie.startsWith("app")
                && trie.search("") && !trie.startsWith("z"), "trie");
        eq(subsets(new int[]{1, 2, 3}).size(), 8, "subsets");
        List<List<Integer>> permutations = uniquePermutations(new int[]{1, 1, 2});
        check(permutations.size() == 3 && new HashSet<>(permutations).size() == 3, "unique permutations");
        eq(subsets(new int[0]).size(), 1, "empty subsets");
        eq(uniquePermutations(new int[0]).size(), 1, "empty permutations");
        eq(coinChange(new int[]{1, 2, 5}, 11), 3, "coin change");
        eq(coinChange(new int[]{2}, 3), -1, "unreachable amount");
        eq(coinChange(new int[0], 0), 0, "zero amount");
        eq(lcs("abcde", "ace"), 3, "lcs"); eq(lcs("", "a"), 0, "empty lcs");
        eq(minPathSum(new int[][]{{1, -2}, {3, -4}}), -5, "negative memo values");
        eq(knapsack(new int[]{2}, new int[]{7}, 4), 7, "knapsack no reuse");
        Set<Cell> cells = new HashSet<>(); cells.add(new Cell(1, 2));
        check(cells.contains(new Cell(1, 2)) && !cells.contains(new Cell(2, 1)), "value key");
    }
    static void randomizedArrays() {
        for (int trial = 0; trial < 300; trial++) {
            int n = RANDOM.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = RANDOM.nextInt(15) - 7;
            int[] sorted = a.clone(); Arrays.sort(sorted);
            int[] merged = a.clone(); mergeSort(merged);
            check(Arrays.equals(merged, sorted), "merge sort oracle");
            for (int target = -8; target <= 8; target++) {
                int lower = 0, upper = 0;
                for (int x : sorted) { if (x < target) lower++; if (x <= target) upper++; }
                eq(lowerBound(sorted, target), lower, "lower bound oracle");
                eq(upperBound(sorted, target), upper, "upper bound oracle");
                long count = 0;
                for (int i = 0; i < n; i++) {
                    long sum = 0;
                    for (int j = i; j < n; j++) { sum += a[j]; if (sum == target) count++; }
                }
                eq(subarraySumCount(a, target), count, "subarray count oracle");
                int[] pair = twoSumSorted(sorted, target);
                boolean exists = false;
                for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++)
                    if ((long) sorted[i] + sorted[j] == target) exists = true;
                check(exists == (pair[0] != -1), "two sum existence");
                if (exists) check(pair[0] < pair[1] && (long) sorted[pair[0]] + sorted[pair[1]] == target, "two sum pair");
            }
            long[] prefix = prefixSums(a);
            Fenwick fenwick = new Fenwick(n);
            for (int i = 0; i < n; i++) fenwick.add(i, a[i]);
            for (int i = 0; i <= n; i++) eq(fenwick.prefix(i), prefix[i], "fenwick prefix");
            for (int i = 0; i < n; i++) {
                fenwick.add(i, 3);
                eq(fenwick.range(i, i + 1), a[i] + 3, "fenwick update");
            }
            int[] next = nextGreaterIndex(a);
            for (int i = 0; i < n; i++) {
                int expected = -1;
                for (int j = i + 1; j < n; j++) if (a[j] > a[i]) { expected = j; break; }
                eq(next[i], expected, "monotonic stack oracle");
            }
            for (int k = 1; k <= n; k++) {
                eq(kthSmallest(a.clone(), k), sorted[k - 1], "quickselect oracle");
                eq(kthLargestHeap(a, k), sorted[n - k], "top-k oracle");
                int[] maximums = slidingMaximum(a, k);
                long bestSum = Long.MIN_VALUE;
                for (int i = 0; i + k <= n; i++) {
                    int max = Integer.MIN_VALUE; long sum = 0;
                    for (int j = i; j < i + k; j++) { max = Math.max(max, a[j]); sum += a[j]; }
                    eq(maximums[i], max, "sliding maximum oracle"); bestSum = Math.max(bestSum, sum);
                }
                eq(maxWindowSum(a, k), bestSum, "window sum oracle");
            }
            if (n > 0) {
                long best = Long.MIN_VALUE;
                for (int i = 0; i < n; i++) for (int j = i + 1; j <= n; j++) best = Math.max(best, prefix[j] - prefix[i]);
                eq(maxSubarray(a), best, "Kadane oracle");
            }
            int bestLis = 0;
            for (int mask = 0; mask < (1 << n); mask++) {
                boolean valid = true; long previous = Long.MIN_VALUE; int length = 0;
                for (int i = 0; i < n; i++) if ((mask & (1 << i)) != 0) {
                    if (a[i] <= previous) valid = false;
                    previous = a[i]; length++;
                }
                if (valid) bestLis = Math.max(bestLis, length);
            }
            eq(lisLength(a), bestLis, "LIS subsequence oracle");
            StringBuilder text = new StringBuilder();
            for (int i = 0; i < n; i++) text.append((char) ('a' + RANDOM.nextInt(4)));
            for (int k = 0; k < 5; k++) {
                int best = 0;
                for (int i = 0; i < n; i++) {
                    Set<Character> seen = new HashSet<>();
                    for (int j = i; j < n; j++) { seen.add(text.charAt(j)); if (seen.size() <= k) best = Math.max(best, j - i + 1); }
                }
                eq(longestAtMostKDistinct(text.toString(), k), best, "variable window oracle");
            }
        }
    }
    static void randomizedGraphs() {
        for (int trial = 0; trial < 100; trial++) {
            int n = 1 + RANDOM.nextInt(7);
            List<List<Edge>> weighted = new ArrayList<>();
            List<int[]> dagEdges = new ArrayList<>();
            long[][] all = new long[n][n];
            for (int i = 0; i < n; i++) { weighted.add(new ArrayList<>()); Arrays.fill(all[i], 1000000); all[i][i] = 0; }
            for (int u = 0; u < n; u++) for (int v = 0; v < n; v++) {
                if (u != v && RANDOM.nextBoolean()) {
                    int weight = RANDOM.nextInt(10);
                    weighted.get(u).add(new Edge(v, weight)); all[u][v] = weight;
                    if (u < v) dagEdges.add(new int[]{u, v});
                }
            }
            for (int k = 0; k < n; k++) for (int u = 0; u < n; u++) for (int v = 0; v < n; v++)
                all[u][v] = Math.min(all[u][v], all[u][k] + all[k][v]);
            for (int source = 0; source < n; source++) {
                long[] distances = dijkstra(weighted, source);
                for (int v = 0; v < n; v++) eq(distances[v], all[source][v] == 1000000 ? Long.MAX_VALUE : all[source][v], "Dijkstra Floyd-Warshall oracle");
            }
            int[][] edges = dagEdges.toArray(new int[0][]);
            int[] order = topologicalSort(graph(n, edges, true));
            eq(order.length, n, "DAG order length");
            int[] position = new int[n]; boolean[] used = new boolean[n];
            for (int i = 0; i < n; i++) { check(!used[order[i]], "topo uniqueness"); used[order[i]] = true; position[order[i]] = i; }
            for (int[] edge : edges) check(position[edge[0]] < position[edge[1]], "topo edge invariant");
            UnionFind unionFind = new UnionFind(n);
            for (int[] edge : edges) unionFind.union(edge[0], edge[1]);
            List<List<Integer>> undirected = graph(n, edges, false);
            eq(unionFind.components, connectedComponents(undirected), "union-find components");
            for (int u = 0; u < n; u++) {
                int[] dist = bfsDistances(undirected, u);
                for (int v = 0; v < n; v++) check((unionFind.find(u) == unionFind.find(v)) == (dist[v] >= 0), "union-find reachability");
            }
        }
    }
    static void randomizedCaches() {
        for (int capacity = 0; capacity <= 5; capacity++) {
            LruCache library = new LruCache(capacity);
            ManualLruCache manual = new ManualLruCache(capacity);
            Map<Integer, Integer> values = new HashMap<>();
            List<Integer> oldestFirst = new ArrayList<>();
            for (int step = 0; step < 1000; step++) {
                int key = RANDOM.nextInt(10);
                if (RANDOM.nextBoolean()) {
                    Integer expected = values.get(key);
                    check(Objects.equals(library.get(key), expected), "library LRU oracle");
                    check(Objects.equals(manual.get(key), expected), "manual LRU oracle");
                    if (expected != null) { oldestFirst.remove(Integer.valueOf(key)); oldestFirst.add(key); }
                } else {
                    int value = RANDOM.nextInt(100);
                    library.put(key, value); manual.put(key, value); values.put(key, value);
                    oldestFirst.remove(Integer.valueOf(key)); oldestFirst.add(key);
                    if (oldestFirst.size() > capacity) values.remove(oldestFirst.remove(0));
                }
            }
        }
    }
    public static void main(String[] args) {
        examples(); randomizedArrays(); randomizedGraphs(); randomizedCaches();
        System.out.println("PASS: " + checks + " checks (examples + randomized oracle comparisons)");
    }
}
