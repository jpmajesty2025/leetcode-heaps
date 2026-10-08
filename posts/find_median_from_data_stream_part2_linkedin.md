# When the Simple Solution Is Fast Enough, and When It Isn't (Part 2 of 2)📏

In Part 1 we solved Find Median from a Data Stream with two heaps. But there's a much simpler idea: **keep a sorted list.**

---

### 🧱 The Sorted-List Version

- `addNum`: binary-search for the right spot and insert, using Python's `bisect.insort`
- `findMedian`: read the middle element, or average the middle two

No invariants to maintain. No balancing step. You can reason about it in seconds, and it's almost impossible to get wrong.

---

### 🔍 What the Cost Really Is

Finding the spot is $\mathcal{O}(\log n)$, but inserting into an array shifts everything after it, which makes `addNum` $\mathcal{O}(n)$ in the worst case. Queries are $\mathcal{O}(1)$.

Theory says the heaps win. So I measured, with one add plus one query per item:

| Items | Two heaps | Sorted list |
| :--- | :--- | :--- |
| 10,000 | ~0.005s | ~0.013s |
| 100,000 | ~0.06s | ~0.6s |
| 500,000 | ~0.3s | ~18s |

I expected the shift to be so fast, since it's a C-level memory move, that the sorted list would hold its own. It doesn't. The gap grows from about 2.5× at 10,000 to about 55× at 500,000. My assumption was wrong, and the measurement caught it.

---

### ⚖️ Trade-off Summary

| Metric | Two Heaps | Sorted List |
| :--- | :--- | :--- |
| **`addNum`** | $\mathcal{O}(\log n)$ | $\mathcal{O}(n)$ worst case |
| **`findMedian`** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Complexity of the code** | Two invariants | Almost none |
| **Scales to millions** | Yes | No |

The sorted list is perfectly fine for the problem's actual limits (up to 50,000 calls). It stops being fine well before a real data stream would.

---

### 🎯 Key Takeaway

"Simpler" and "scalable" are different axes. Pick the simple one when the input is bounded and small, and know the point where it breaks. Then **measure**, don't guess.

Both versions pass the same test suite and agree on every random stream I generated.

Have you ever been surprised by a benchmark that disproved your assumption? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BigO #Benchmarking #Tradeoffs #LeetCode #SoftwareEngineering #CodingInterview
