# Two Heaps, One Median: Solving Find Median from a Data Stream (Part 1 of 2) 🎯

**The Problem**:
Design a `MedianFinder` class that supports `addNum(num)` and `findMedian()` on a growing stream of integers. The median is the middle value of the sorted data, or the mean of the two middle values when the count is even.

Re-sorting on every query costs $\mathcal{O}(n \log n)$ per call. But here's the key observation: **we never need the whole sorted order. We only need the middle.**

---

### 💡 The Idea: Split the Data in Half

Keep two heaps:

1️⃣ **Lower half** in a **max-heap**, so its top is the largest of the small values
2️⃣ **Upper half** in a **min-heap**, so its top is the smallest of the large values

If the halves stay balanced, the median is sitting right at the tops. No sorting is needed.

Python's `heapq` is min-only (before 3.14), so the lower half stores negated values.

---

### 🔧 Two Invariants Do All the Work

- Every value in the lower half is $\le$ every value in the upper half
- The lower half is the same size as the upper half, or exactly one larger

On `addNum`:
1. Push the new value through the lower half, then move that half's maximum to the upper half. This keeps the ordering correct, no matter where the value belongs.
2. If the upper half now has more elements, move its minimum back down.

On `findMedian`:
- Odd count: the top of the lower half
- Even count: the average of both tops

---

### ⚠️ Details That Bite

- **Duplicates** are fine, because the ordering rule uses $\le$.
- **Negatives and zero** are fine. The negation trick doesn't care.
- **An exact median of zero** (like $-5$ and $5$) is a good test.
- **Empty queries** are outside the contract. I let `IndexError` surface instead of returning a fake value.

---

### 📊 Complexity

| Operation | Time | Space |
| :--- | :--- | :--- |
| `addNum` | $\mathcal{O}(\log n)$ | |
| `findMedian` | $\mathcal{O}(1)$ | |
| **Total** | | $\mathcal{O}(n)$ |

---

### 🎯 Key Takeaway

When you need the middle of a changing dataset, you don't need it sorted. Split it into two halves and keep only the boundary visible.

Where else have you used the two-heaps pattern? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #TwoHeaps #LeetCode #SoftwareEngineering #CodingInterview
