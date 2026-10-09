# Beating the Heap: When Counting Buckets Wins...and When It Doesn't (Part 1 of 2) 🪣

In Part 1, a max-heap solved Remove Stones to Minimize the Total in $\mathcal{O}(n + k \log n)$. But the problem has a hidden structure: pile sizes are **small integers** (up to 10,000 on LeetCode). That opens a different data structure.

---

### 💡 The Idea: Count Piles by Size

Instead of a heap of piles, keep an array where position $s$ stores how many piles currently have exactly $s$ stones. Then sweep from the largest size down to 2:

1️⃣ At size $s$, halve as many piles as the remaining budget allows
2️⃣ Move them to bucket $\lceil s/2 \rceil$
3️⃣ Reduce the budget by that count and keep sweeping

---

### 🔑 Why Bulk Processing Is Safe

For $s \ge 2$, $\lceil s/2 \rceil < s$. A halved pile always lands in a **strictly smaller** bucket, so the sweep never needs to look back up. The greedy order (largest first) is preserved automatically, and a whole bucket can move at once instead of one pile at a time.

Size 1 can't shrink, so the sweep stops at 2.

---

### 📊 Heap vs. Buckets

| Metric | Max-Heap | Counting Buckets |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(n + k \log n)$ | $\mathcal{O}(n + M)$ |
| **Space** | $\mathcal{O}(n)$ | $\mathcal{O}(M)$ |
| **Depends on value range** | No | **Yes** ($M$ = max pile) |
| **Code complexity** | Simple | Simple |

---

### ⏱️ What I Measured

$n = k = 100{,}000$:

| Max pile size | Heap | Buckets |
| :--- | :--- | :--- |
| 10,000 (LeetCode limit) | ~0.045s | ~0.006s |
| 10,000,000 | ~0.054s | ~1.8s |

Within the problem's real constraints, buckets are about **8× faster**. Remove that bound and the picture flips: the bucket array becomes huge and the heap is about **34× faster**.

Both versions returned identical answers on every random test, and both passed the same exhaustive-search check for optimality.

---

### 🎯 Key Takeaway

Constraints are part of the algorithm. A small bounded value range is a hint to consider counting-based approaches, but the speedup depends entirely on that bound. Know which assumption your optimization is leaning on.

When have you traded generality for speed because the input range allowed it? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #CountingSort #Heap #Tradeoffs #LeetCode #SoftwareEngineering #CodingInterview
