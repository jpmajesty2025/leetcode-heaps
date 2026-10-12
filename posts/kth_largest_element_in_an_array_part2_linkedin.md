# Beating O(n log k): Quickselect & Dutch Flags (Part 2 of 2) ⚡

In Part 1, a size-$k$ min-heap solved Kth Largest Element in $\mathcal{O}(n \log k)$ time and $\mathcal{O}(k)$ space. But can we drop the logarithm and hit linear time?

Yes—with **Quickselect (Hoare's Selection Algorithm)**.

---

### 🎯 The Linear-Time Intuition

Quicksort partitions an array around a pivot and recurses on **both** sides in $\mathcal{O}(n \log n)$.

Quickselect uses the same partition step, but the target rank lives in only **one** side. We discard the other partition entirely.

The work shrinks geometrically: $n + n/2 + n/4 + \dots = \mathcal{O}(n)$ average time! An iterative loop keeps auxiliary space at $\mathcal{O}(1)$.

---

### ⚠️ The Two Deadly Pitfalls in Quickselect

Textbook Quickselect looks simple, but two edge cases degrade it to $\mathcal{O}(n^2)$:

1️⃣ **Pre-sorted arrays**: Fixed pivots peel off only 1 element per step.
➡️ **Fix**: Choose a random pivot index.

2️⃣ **Massive duplicates**: With 100,000 identical numbers, naive 2-way partitioning lumps all duplicates into one side, triggering $\mathcal{O}(n^2)$.
➡️ **Fix**: **3-Way Partitioning (Dutch National Flag)**. Divide the array into `< pivot`, `== pivot`, and `> pivot`. All elements matching the pivot resolve in a single step!

---

### 🪣 The Bounded-Range Alternative: Counting Sort

When values fall within a bounded integer range (e.g., LeetCode's $[-10^4, 10^4]$), comparison algorithms can be skipped entirely. Count frequencies into an array of size $20{,}001$, then scan downward from the maximum until $k$ elements accumulate.

This gives **deterministic** $\mathcal{O}(n + M)$ time with no recursion and no worst-case variance.

---

### ⚖️ Trade-offs

| Metric | Min-Heap | 3-Way Quickselect | Bounded Counting |
| :--- | :--- | :--- | :--- |
| **Time** | $\mathcal{O}(n \log k)$ | $\mathcal{O}(n)$ average | $\mathcal{O}(n + M)$ deterministic |
| **Aux Space** | $\mathcal{O}(k)$ | $\mathcal{O}(1)$ | $\mathcal{O}(M)$ |
| **Best When** | Streaming data | General arrays | Small bounded range |
| **Worst Case** | Deterministic | $\mathcal{O}(n^2)$ (rare) | Large range |

---

### 🎯 Key Takeaway

Heaps shine for streaming data, Quickselect delivers in-place $\mathcal{O}(n)$ selection, and counting sort wins when constraints bound the range.

Which approach do you reach for first in interviews? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Quickselect #BigO #LeetCode #SoftwareEngineering #CodingInterview
