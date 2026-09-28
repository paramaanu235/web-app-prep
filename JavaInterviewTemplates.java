import java.util.*;

/** Java 8-compatible interview templates. Read each method's contract before reuse. */
public class JavaInterviewTemplates {
    // BEGIN 01 | Arrays and lists | Essential
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
    // END

    // BEGIN 02 | Strings and characters | Essential
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
    // END

    // BEGIN 03 | HashMap and HashSet | Essential
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
    // END

    // BEGIN 04 | Queue stack and deque | Essential
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
    // END

    // BEGIN 05 | Heaps comparators and top-k | Essential
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
    // END

    // BEGIN 06 | Ordered maps sets and multisets | Essential
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
        if (counts.get(x) == 1) counts.remove(x);
        else counts.put(x, counts.get(x) - 1);
        NavigableSet<Integer> set = new TreeSet<>();
        set.add(10); set.add(20);
        Integer candidate = set.ceiling(11);
        // TreeSet removes duplicates according to its comparator (compare == 0).
    }
    // END

    // BEGIN 07 | Numeric safety and bit operations | Essential
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
    // END

    // BEGIN 08 | Node definitions | Essential
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
    // END

    // BEGIN 09 | Linked-list reverse cycle and merge | Essential
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
    // END

    // BEGIN 10 | Binary-search boundaries | Essential
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
    // END

    // BEGIN 11 | Binary search on the answer | Essential
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
    // END

    // BEGIN 12 | Prefix sums and subarray-sum counting | Essential
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
    // END

    // BEGIN 13 | Two pointers on sorted input | Essential
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
    // END

    // BEGIN 14 | Variable sliding window | Essential
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
    // END

    // BEGIN 15 | Fixed sliding window | Essential
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
    // END

    // BEGIN 16 | Monotonic stack | Essential
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
    // END

    // BEGIN 17 | Monotonic deque for sliding maximum | Important
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
    // END

    // BEGIN 18 | Merge intervals | Essential
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
    // END

    // BEGIN 19 | Meeting rooms and endpoint semantics | Important
    static int meetingRooms(int[][] intervals) {
        // Half-open intervals [start,end), start < end; touching meetings coexist.
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
    // END

    // BEGIN 20 | Tree inorder and level-order traversal | Essential
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
    // END

    // BEGIN 21 | Tree recursion balance and LCA | Essential
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
    // END

    // BEGIN 22 | Validate a BST with bounds | Essential
    static boolean validBST(TreeNode root) {
        return validBST(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    static boolean validBST(TreeNode node, long low, long high) {
        if (node == null) return true;
        if (node.val <= low || node.val >= high) return false;
        return validBST(node.left, low, node.val) && validBST(node.right, node.val, high);
    }
    // Strict BST: duplicates disallowed. O(n), O(h). Long bounds admit all int values.
    // END

    // BEGIN 23 | Graph construction DFS and BFS distances | Essential
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
    // END

    // BEGIN 24 | Grid and multi-source BFS | Essential
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
    // END

    // BEGIN 25 | Topological sort and directed cycle detection | Essential
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
    // END

    // BEGIN 26 | Dijkstra with stale-entry skipping | Essential
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
    // END

    // BEGIN 27 | Union-find with size and path compression | Essential
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
    // END

    // BEGIN 28 | Trie insert search and prefix | Essential
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
    // END

    // BEGIN 29 | Backtracking subsets and unique permutations | Essential
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
    // END

    // BEGIN 30 | Bottom-up DP coin change | Essential
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
    // END

    // BEGIN 31 | Two-dimensional DP longest common subsequence | Essential
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
    // END

    // BEGIN 32 | Top-down memoization | Essential
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
    // END

    // BEGIN 33 | Longest increasing subsequence | Important
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
    // END

    // BEGIN 34 | Merge sort | Important
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
    // END

    // BEGIN 35 | Randomized three-way quickselect | Stretch
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
    // END

    // BEGIN 36 | Fenwick tree for point updates and range sums | Stretch
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
    // END

    // BEGIN 37 | LRU cache using library primitives | Important
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
    // END

    // BEGIN 38 | Immutable composite hash-map key | Important
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
    // END

    // BEGIN 39 | Kadane maximum subarray | Essential
    static long maxSubarray(int[] a) {
        if (a.length == 0) throw new IllegalArgumentException("nonempty array required");
        long endingHere = a[0], best = a[0];
        for (int i = 1; i < a.length; i++) {
            endingHere = Math.max((long) a[i], endingHere + a[i]);
            best = Math.max(best, endingHere);
        }
        return best; // nonempty subarray; O(n), O(1); handles all-negative input
    }
    // END

    // BEGIN 40 | One-dimensional 0-1 knapsack | Important
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
    // END

    // BEGIN 41 | LRU internals hash map and doubly linked list | Important
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
    // END

    // BEGIN 42 | Bipartite graph coloring | Important
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
    // END
}
