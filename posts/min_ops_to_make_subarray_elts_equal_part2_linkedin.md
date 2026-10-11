# No Heaps, No Lazy Deletion: A Fenwick Tree for the Sliding Median (Part 2 of 2)🌲

In Part 1, two heaps with lazy deletion solved Minimum Operations to Make Subarray Elements Equal in $\mathcal{O}(n \log n)$. It works, but lazy deletion is fiddly. Is there a structure where removing an element is as natural as adding one?

---

### 💡 The Idea: A Window That Supports Rank Queries

Every window needs three things:
1. The **median**: the $\lceil k/2 \rceil$-th smallest element
2. The **count and sum** of everything at or below the median
3. The window's total sum, which is easy to track as it slides

A **Fenwick tree (binary indexed tree)** over the values answers all of this, one tree for counts and one for sums.

---

### 🔧 How It Works

1️⃣ **Compress coordinates**: map each distinct value to a rank $1..m$
2️⃣ **Slide**: add the new element and subtract the outgoing one, each in $\mathcal{O}(\log m)$ with a signed update. Removal is just a `-1`.
3️⃣ **Find the median** by binary descent on the count tree: walk down the tree to the first rank whose prefix count reaches $\lceil k/2 \rceil$
4️⃣ **Get count and sum at or below the median** from one prefix query
5️⃣ **Compute the cost** from those and the window total

No rebalancing, no pending-deletion map, no heap invariants to keep in sync.

---

### 📊 Heaps vs. Fenwick

| Metric | Two Heaps + Lazy Deletion | Fenwick Trees |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ |
| **Space** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ |
| **Removal** | Deferred (lazy) | Immediate (`-1` update) |
| **Needs value compression** | No | Yes |
| **Edge cases** | Ties and stale tops | Few |

Same asymptotics, so I measured ($n = 100{,}000$):

| Window size $k$ | Heaps | Fenwick |
| :--- | :--- | :--- |
| 100 | ~0.31s | ~0.65s |
| 50,000 | ~0.20s | ~0.53s |

The heaps were about **2 to 3× faster** here. Python's `heapq` runs in C, while my Fenwick loops run in pure Python bytecode. Same big-O doesn't mean same speed.

Both returned identical answers on every random and duplicate-heavy test, and both matched the brute-force baseline.

---

### 🎯 Key Takeaway

Pick a structure for how simply it models the problem, then measure. The Fenwick version has fewer special cases and is easier to trust. The heap version is faster in this language. Both are valid, and which one wins depends on what you're optimizing for.

Do you reach for the faster structure or the simpler one first? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #FenwickTree #BinaryIndexedTree #SlidingWindow #LeetCode #SoftwareEngineering #CodingInterview
