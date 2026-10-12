# When O(n) Quickselect Loses to O(n log k) Heap (Part 2 of 2) ⚡

In Part 1, a size-k max-heap solved K Closest Points to Origin in O(n log k) time. But the problem gives a clue: **"You may return the answer in any order."**

If we don't need the k points sorted, can we hit linear time? Yes—with **Quickselect (Hoare's Selection)**.

---

### 🎯 The Linear-Time Intuition

Quicksort partitions around a pivot and sorts both sides in O(n log n). Quickselect only recurses into the side containing boundary k.

The work shrinks geometrically: n + n/2 + n/4 + ... = O(n) average time!

Using **3-Way Partitioning (Dutch National Flag)** groups points on the same distance circle (e.g. [1, 3] and [-3, 1]) together, resolving ties in a single pass without quadratic slowdown.

---

### 😬 Then I Benchmarked It (n = 100,000)

Textbook theory says O(n) Quickselect should beat O(n log k) Heap. But hardware cares about constant factors:

| Scenario (n=100k) | Size-k Heap | 3-Way Quickselect | Winner |
| :--- | :--- | :--- | :--- |
| k = 10 | **0.016s** | 0.038s | **Heap (2.4x faster)** |
| k = 1,000 | **0.018s** | 0.020s | **Heap (1.1x faster)** |
| k = 50,000 | **0.066s** | 0.133s | **Heap (2.0x faster)** |

Why does the heap win in practice?
1️⃣ **Early Filtering**: For small k, >99.9% of points are rejected with a single O(1) check once the root settles. Quickselect still partitions and swaps elements.
2️⃣ **C vs Python**: Python's `heapq` runs in compiled C. Quickselect's array swaps run in Python bytecode.

---

### ⚖️ The Real-World Trade-off

- **Size-k Heap**: wins when k << n or with streaming data where n is unknown. Memory stays capped at O(k) and early filtering dominates.
- **Quickselect**: wins when k is close to n, memory must be O(1), or in C/C++ where in-place pointer swaps are instant.

---

### 🧪 How I Verified It

I tested both implementations with a 47-test suite and Hypothesis:
- Boundary conditions: k = 1, k = n, origin [0,0], negatives
- Rotational symmetry: reflecting across the origin preserves distances
- Invariant: proved no excluded point is closer than any included point

---

### 🎯 Key Takeaway

Big-O describes asymptotic trends, not wall-clock speed. When k is small, a bounded heap's O(1) rejection filter beats linear partitioning in practice.

Has a higher-complexity algorithm ever beaten an "optimal" one in your benchmarks? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Quickselect #Benchmarking #BigO #LeetCode #SoftwareEngineering #CodingInterview
