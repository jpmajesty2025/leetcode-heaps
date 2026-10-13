# The Delimiter Invariant: Constructing Repeat-Limited Strings (Part 1 of 2) 🔤

**The Problem**:
Given a string $s$ and an integer `repeatLimit`, construct the **lexicographically largest** string using the characters of $s$ such that no letter appears more than `repeatLimit` times consecutively. You do not have to use all characters.

At first glance, it looks like standard frequency sorting. But respecting repeat limits while maintaining lexicographical rank introduces a strict greedy rule.

---

### 🎯 The Greedy Intuition

To maximize lexicographical rank, later alphabet letters ('z' before 'y', 'y' before 'x') must appear as early as possible.

At any step:
1️⃣ Pick the largest available character $c_1$.
2️⃣ Append as many copies of $c_1$ as allowed: `use = min(count, repeatLimit)`.

If all copies of $c_1$ are exhausted, we move to the next largest letter.

But what if $c_1$ has copies left?

---

### 🧱 The 1-Character Delimiter Invariant

If $c_1$ has remaining copies, appending another $c_1$ violates `repeatLimit`.

To use $c_1$ again, we MUST break the streak with a different character.

To maintain maximum lexicographical rank:
- **Which character should we use as delimiter?** The *next largest* available character $c_2$ ($c_2 < c_1$).
- **How many copies of $c_2$ should we append?** **EXACTLY ONE!**

Why only one? Because every extra copy of $c_2$ placed now is inferior to placing the remaining copies of higher-value character $c_1$ as soon as possible!

If no smaller character $c_2$ exists, we cannot break the streak and must stop immediately.

---

### 💥 The Critical Push-Back Bug

In heap implementations, a common bug is popping $c_2$ from the max-heap, appending one copy, and **forgetting to push back the remaining `count - 1` copies of $c_2$**!

When that happens, all remaining copies of $c_2$ vanish, corrupting the result.

Both $c_1$ and $c_2$ must be returned to the heap with their updated counts.

---

### 📊 Complexity

- **Time:** O(n + |Σ| log |Σ|) where $|Σ| \le 26$ is alphabet size
- **Space:** O(|Σ|) auxiliary space for heap and counts

---

### 🎯 Key Takeaway

Place the largest available character up to the limit, and use exactly one delimiter character to unlock remaining high-value letters.

In Part 2, we'll see why a 26-element array can bypass the heap entirely.

Have you encountered greedy problems where delimiter choices dictate the outcome? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #Greedy #LeetCode #SoftwareEngineering #CodingInterview
