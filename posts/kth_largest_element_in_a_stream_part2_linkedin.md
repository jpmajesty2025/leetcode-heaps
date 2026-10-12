# Bounded Heap vs. Sorted List in Real-Time Systems (Part 2 of 2) ⏱️

In Part 1, we used a size-$k$ min-heap to track the $k$-th highest score in real time with O(log k) updates and O(k) memory.

Python offers a simple alternative: **keep a bounded sorted list using `bisect`**.

---

### 🧱 The Bounded Sorted-List Idea

Keep the top $k$ scores in a sorted Python list:
- Binary-search the insertion index in O(log k) with `bisect.insort`
- Pop the smallest element if size exceeds $k$
- Reading the $k$-th largest is a direct O(1) index on the first element

No heap invariants, simple to implement.

---

### 😬 Then I Benchmarked It (Stream of 100,000 Scores)

Both approaches cap memory at $k$ elements. But how do they scale as $k$ grows?

| Scenario ($n=100\text{k}$) | Size-$k$ Heap | Bounded Sorted List | Winner |
| :--- | :--- | :--- | :--- |
| $k = 5$ | **0.016s** | 0.019s | **Heap (1.2x faster)** |
| $k = 100$ | **0.017s** | 0.045s | **Heap (2.6x faster)** |
| $k = 1{,}000$ | **0.016s** | 0.098s | **Heap (6.1x faster)** |

At $k = 5$, both are fast. But by $k = 1{,}000$, the sorted list takes 6× longer!

---

### 🔍 Why the Gap Widens as $k$ Grows

1️⃣ **Tree Sifting vs. Array Shifting**:
When a score beats the cutoff, a heap sifts along a tree branch of height $\log_2 k$. For $k = 1{,}000$, that's at most 10 pointer swaps. A sorted list shifts up to 1,000 array elements in memory via `memmove`!

2️⃣ **The Unbounded Trap**:
Without capping the list at $k$, inserting into a 100,000-item array degrades to O(n) per score, causing $\mathcal{O}(n^2)$ total work and unbounded memory growth.

---

### ⚖️ The Real-World Trade-off

- **Bounded Heap**: The clear winner for real-time streams and larger $k$. Updates stay O(log k) and memory is bounded to O(k).
- **Sorted List (`bisect`)**: Great for tiny $k$ ($k \le 10$) where cache locality dominates and simplicity is preferred.

---

### 🧪 How I Verified It

I tested both implementations with a 29-test suite and Hypothesis:
- Edge cases: $k=1$ (running maximum), empty initial array, duplicates, negatives
- Proved non-decreasing monotonicity: the cutoff mark never drops
- Verified shift invariance and 100% agreement with an independent sorting oracle

---

### 🎯 Key Takeaway

For unbounded streams, always cap state. A bounded min-heap keeps memory tight and latency minimal, avoiding hidden memory shifting costs in real-time pipelines.

Have you seen in-memory array shifts bottleneck streaming services? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #StreamingData #Benchmarking #LeetCode #SoftwareEngineering #CodingInterview
