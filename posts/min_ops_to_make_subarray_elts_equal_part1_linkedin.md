# Sorting Broke My Subarray: Sliding-Window Median with Two Heaps (Part 1 of 2) 🪟

**The Problem:**
Given an array `nums` and an integer $k$, you may add or subtract 1 from any element. Return the minimum operations to make at least one **subarray of size $k$** all equal.

My first attempt: sort the array, slide a window, and raise each element to the window's max with prefix sums. Fast, tidy, and wrong for two separate reasons.

---

### 🐛 Two Bugs in One Idea

1️⃣ **Sorting destroys "subarray".** Subarrays must be contiguous in the *original* order. Sorting makes distant elements neighbors.
Example: `[5, 1, 5, 1]` with $k = 2$. Sorted gives `[1, 1]` (cost 0), but in the real array every adjacent pair is `[5, 1]` or `[1, 5]` (cost **4**).

2️⃣ **Raising to the max is suboptimal.** Since we can increase *and* decrease, the target shouldn't be the max. For `[1, 100, 2]` with $k = 3$, targeting 100 costs 197, while targeting 2 costs **99**.

---

### 💡 The Right Target: The Median

The value minimizing $\sum |x - t|$ is the **median**. So each window's cost is the sum of distances to its median, and we want the cheapest window **in the original order**.

Sorting every window takes $\mathcal{O}(n \cdot k \log k)$—too slow. We need the median and distance sum dynamically as the window slides.

---

### 🔧 Two Heaps, Plus Sums

Like *Find Median from a Data Stream*:
- A **max-heap** for the lower half (including the median)
- A **min-heap** for the upper half
- Running sums of each half

With median $m$, the window cost is:
$$m \cdot |\text{low}| - \sum \text{low} + \sum \text{high} - m \cdot |\text{high}|$$

Heaps can't delete from the middle, so removals are **lazy**: mark outgoing values as pending and pop them once they surface at a heap top. Sizes and sums track only live elements.

**Complexity:** $\mathcal{O}(n \log n)$ time, $\mathcal{O}(n)$ space.

---

### 🧪 How I Trusted It

Lazy deletion with duplicates is where bugs hide, so I tested thoroughly:
- Re-sorting every window from scratch as the baseline
- Inputs drawn from just 5 distinct values to force ties
- An exhaustive check that **no target beats the median**
- Invariant tests: shifting values by $+c$, scaling by 3, and reversing the array

---

### 🎯 Key Takeaway

A pattern for "only increase" fails when you can also decrease, and sorting destroys subarray contiguity. Always verify constraints before reusing a trick.

Have you ever shipped a clean solution that solved the wrong problem? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #SlidingWindow #Median #LeetCode #SoftwareEngineering #CodingInterview
