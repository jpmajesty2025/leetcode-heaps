# Bounded Heap vs. Full Heap vs. Buckets: Top-K Words Benchmarked (Part 2 of 2) 📊

In Part 1, we used a size-$k$ min-heap with a custom comparator to solve Top K Frequent Words in O(n + m log k) time.

Can we avoid writing a custom class in interviews? Yes—in two distinct ways.

---

### 💡 Alternative 1: The Full Max-Heap `(-freq, word)`

Instead of capping the heap at size $k$, store all $m$ unique words in a heap of `(-freq, word)` tuples:
- `-freq`: Higher frequency produces a smaller negative number
- `word`: On ties, the alphabetically smaller word compares smaller

Because both keys sort ascending natively, standard tuple comparison works out of the box!
- `heapify` in O(m) time
- `heappop` $k$ times in O(k log m) time

---

### 🪣 Alternative 2: Frequency Buckets

A word appears at most $n$ times.
1️⃣ Count frequencies with a hash map
2️⃣ Place each distinct word in `buckets[freq]`
3️⃣ Walk from the highest frequency down, sorting words within each bucket alphabetically until $k$ words accumulate

No heaps, no sifting, and linear O(n) average time!

---

### 😬 Then I Benchmarked Them (200k tokens, 10k unique words)

| Scenario ($n=200\text{k}$) | Bounded Heap | Full Heap | Buckets | Winner |
| :--- | :--- | :--- | :--- | :--- |
| $k = 10$ | 0.017s | 0.015s | **0.007s** | **Buckets (2.4x faster)** |
| $k = 100$ | 0.012s | 0.010s | **0.009s** | **Buckets (1.3x faster)** |
| $k = 1{,}000$ | 0.017s | 0.009s | **0.008s** | **Buckets (2.1x faster)** |

Why does the bounded heap lose in Python despite better big-O?
1️⃣ **Object Overhead**: Instantiating $m$ wrapper objects and invoking Python `__lt__` during sifts adds latency.
2️⃣ **C Speed**: Full Heap and Buckets run in compiled C (`heapify` on C tuples, Timsort on string arrays).

---

### ⚖️ The Real-World Trade-off

- **Bounded Heap**: The right choice when $m$ is massive and memory must stay capped at O(k) (streaming data).
- **Full Heap**: The fastest interview solution to write—clean, 4 lines of code, no custom classes.
- **Buckets**: The fastest in execution time when processing batch text.

---

### 🧪 How I Verified It

I tested both implementations with a 35-test suite and Hypothesis:
- Strict ordering invariant: frequencies are non-increasing; ties are strictly alphabetical
- 100% agreement between implementations across random vocabularies

---

### 🎯 Key Takeaway

Big-O guides architecture, but runtime details dictate real-world speed. In Python, native C-backed data structures often beat theoretical big-O advantages burdened with custom object overhead.

Which pattern do you prefer for compound tie-breakers? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #Benchmarking #TopK #LeetCode #SoftwareEngineering #CodingInterview
