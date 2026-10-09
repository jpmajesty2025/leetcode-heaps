# Do You Even Need the Heap? The Two-Queue Trick (Part 2 of 2) 🚂

In Part 1, a min-heap solved Minimum Cost to Connect Sticks in $\mathcal{O}(n \log n)$. But the greedy process has a pattern the heap doesn't exploit.

---

### 🔍 The Observation

Each merge combines the two smallest values. The next merge's two smallest values can never be smaller than the last pair's. So the **merged sticks are produced in non-decreasing order**.

If new sticks arrive already sorted, you don't need a heap to keep them ordered. A plain **FIFO queue** does it for free.

---

### 🔧 The Two-Queue Approach

1️⃣ **Sort** the original sticks once and put them in a queue
2️⃣ Keep a second, initially empty queue for merged sticks
3️⃣ For each of the $n - 1$ merges, take the smaller of the two queue fronts, twice
4️⃣ Add the sum to the total and append it to the merged queue

Both queues stay sorted, so the two smallest sticks are always sitting at the fronts. No heap pushes, no heap pops, no sift operations.

---

### 📊 Heap vs. Two Queues

| Metric | Min-Heap | Two Queues |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ sort + $\mathcal{O}(n)$ merge |
| **Space** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ |
| **Merge phase** | Heap ops, $\mathcal{O}(\log n)$ each | Queue ops, $\mathcal{O}(1)$ each |
| **Key requirement** | None | Merged values arrive in sorted order |

The asymptotic bound is the same, because the sort still costs $\mathcal{O}(n \log n)$. The question is the constant factor, so I measured it (best of three runs):

| Sticks | Heap | Two queues |
| :--- | :--- | :--- |
| 10,000 | ~0.005s | ~0.003s |
| 100,000 | ~0.074s | ~0.041s |
| 1,000,000 | ~1.6s | ~0.59s |

The two-queue version is consistently faster, about 1.7× at 10,000 sticks and 2.7× at a million. Sorting in C beats maintaining a heap in Python.

Both returned identical answers on every random input I generated, and both matched the exhaustive-search check.

---

### 🎯 Key Takeaway

A heap is the general tool for "keep the minimum available as things change." If you can prove the new items arrive in order, a queue is enough. Look for monotonicity in your own data before you reach for the heavier structure.

The same trick shows up in the classic linear-time Huffman construction. Have you used it elsewhere? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Queue #Greedy #Optimization #LeetCode #SoftwareEngineering #CodingInterview
