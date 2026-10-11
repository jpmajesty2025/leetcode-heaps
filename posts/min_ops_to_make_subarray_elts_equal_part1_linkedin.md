# Sorting Broke My Subarray: Sliding-Window Median with Two Heaps (Part 1 of 2) 🪟

**The Problem**:
Given an array `nums` and an integer $k$, you may add or subtract 1 from any element, any number of times. Return the minimum operations so that at least one **subarray of size $k$** has all elements equal.

My first attempt was a familiar pattern: sort the array, slide a window over it, and raise every element to the window's largest value using prefix sums. It's fast and tidy, and wrong for two separate reasons.

---

### 🐛 Two Bugs in One Idea

1️⃣ **Sorting destroys "subarray".** A subarray is contiguous in the *original* order. After sorting, windows contain elements that were never neighbors.
Example: `[5, 1, 5, 1]` with $k = 2$. Sorted, the window `[1, 1]` costs 0. In the real array, every pair is `[5, 1]` or `[1, 5]`, so the answer is **4**.

2️⃣ **Raising to the max isn't optimal.** This problem allows increases *and* decreases. Take `[1, 100, 2]` with $k = 3$: raising everything to 100 costs 197, but moving to 2 costs only **99**.

---

### 💡 The Right Target: The Median

For a set of numbers, the value that minimizes the total absolute distance $\sum |x - t|$ is the **median**. So a window's cost is the sum of distances to its median, and the answer is the cheapest window **in the original order**.

Sorting every window costs $\mathcal{O}(n \cdot k \log k)$, which is too slow. We need the median and distance sum as the window slides.

---

### 🔧 Two Heaps, Plus Sums

Same structure as Find Median from a Data Stream:
- A **max-heap** for the lower half (including the median)
- A **min-heap** for the upper half
- Running sums of each half

With the median $m$, the window cost is
$$m \cdot |\text{low}| - \sum \text{low} + \sum \text{high} - m \cdot |\text{high}|$$

Heaps can't delete from the middle, so removals are **lazy**: mark the outgoing value as pending and discard it once it reaches a heap top. Sizes and sums count only live elements.

**Complexity:** $\mathcal{O}(n \log n)$ time, $\mathcal{O}(n)$ space.

---

### 🧪 How I Trusted It

Lazy deletion with duplicates is where bugs hide, so I tested hard there:
- Every contiguous window re-sorted from scratch as the baseline
- Arrays drawn from only 5 distinct values, to force ties
- An exhaustive check that **no target value beats the median**
- Properties: shifting every value leaves the answer unchanged, scaling by 3 triples it, and reversing the array changes nothing

---

### 🎯 Key Takeaway

A pattern that works for "only increase" doesn't transfer to "increase or decrease," and sorting quietly changes what a subarray means. Re-read the constraints before reusing a trick.

Have you shipped a clean-looking solution that solved a different problem than the one asked? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #SlidingWindow #Median #LeetCode #SoftwareEngineering #CodingInterview
