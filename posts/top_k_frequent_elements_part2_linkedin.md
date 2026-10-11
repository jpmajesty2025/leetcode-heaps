# "O(n) Beats O(n log k)", Until I Benchmarked It 🪣

In Part 1, a size-$k$ min-heap solved Top K Frequent Elements in $\mathcal{O}(n + m \log k)$. But there's a textbook way to drop the log entirely: **bucket sort by frequency.**

---

### 💡 The Idea

A value can appear at most $n$ times, so frequencies live in a small range. Instead of ranking values with a heap, drop each one into the bucket for its count, then read the buckets from the highest count down until you've collected $k$ values.

1️⃣ Count values with a hash map
2️⃣ Place each distinct value in `buckets[count]`
3️⃣ Walk the buckets from the highest frequency down, collecting values until you have $k$

No heap, no comparisons, and $\mathcal{O}(n)$ time and space.

---

### 😬 Then I Measured It

My first version allocated $n + 1$ empty buckets, one for every possible frequency. With a million elements, that's a million empty lists, and **it ran 2× to 14× slower than the heap**, even though its big-O was better.

The fix: size the bucket array by the **highest frequency actually present**, not by $n$. For random data that's a few dozen buckets instead of a million.

($n = 1{,}000{,}000$, best of three runs)

| Scenario | Heap | Buckets (first try) | Buckets (fixed) | `most_common` |
| :--- | :--- | :--- | :--- | :--- |
| 100k distinct, $k=10$ | 0.095s | 0.646s | 0.085s | 0.073s |
| 100k distinct, $k=50{,}000$ | 0.145s | 0.587s | 0.081s | 0.159s |
| 1k distinct, $k=10$ | 0.037s | 0.503s | 0.038s | 0.038s |
| All distinct, $k=10$ | 0.329s | 0.646s | 0.194s | 0.186s |

After the fix, buckets are competitive everywhere and clearly faster when $k$ is large. Python's built-in `Counter.most_common` (itself a heap-based top-$k$) stays right alongside it.

---

### ⚖️ Trade-offs

| Metric | Size-$k$ Heap | Frequency Buckets |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(n + m \log k)$ | $\mathcal{O}(n)$ |
| **Extra space** | $\mathcal{O}(m + k)$ | $\mathcal{O}(n)$ worst case |
| **Wins when** | $k$ is small | $k$ is large |
| **Pitfall** | None notable | Over-allocating buckets |

Both pass the same property-based suite, and they return the same frequency profile on every random input.

---

### 🎯 Key Takeaway

Big-O describes growth, not constant factors. An "optimal" algorithm with a careless allocation can lose badly to a simpler one. Benchmark, find the real cost, then fix that.

Has a theoretically better algorithm ever lost to a simpler one in your testing? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BucketSort #Benchmarking #BigO #LeetCode #SoftwareEngineering #CodingInterview
