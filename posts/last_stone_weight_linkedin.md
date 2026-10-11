# Python's heapq Had No Max-Heap (Until 3.14). The Negation Trick to Create a Max-Heap 🪨

**The Problem**:
Given an array of stone weights, repeatedly smash the two heaviest stones together. If they're equal, both vanish. Otherwise the heavier one survives with the difference. Return the weight of the last stone, or `0` if none remain.

Every turn asks for the same thing: *"give me the maximum, twice, then insert a new value (maybe)."* That's a textbook **priority queue**. But before Python 3.14, `heapq` only ships a **min-heap**. (3.14 adds `heapify_max`, `heappush_max` and `heappop_max`. I'm on 3.11, so negation is my path to a max-heap.)

---

### 💡 The Trick: Store Negatives

Negate every weight on the way in. The smallest value in the min-heap now represents the heaviest stone. For instance, if the heaviest stone is 10, then -1 is at the root of this min-heap, effectively turning it into a max-heap.

1️⃣ **Build in linear time**: `heapify` turns the negated list into a heap in $\mathcal{O}(n)$, instead of $n$ pushes at $\mathcal{O}(n \log n)$.
2️⃣ **Smash**: pop two values, and if they differ, push their difference back.
3️⃣ **Stay in negative space**: the first pop is always the heaviest, so the difference of the two negatives is already the correct negative result. No `abs()` calls needed.
4️⃣ **Answer**: negate the survivor, or return `0` if the heap is empty.

---

### 📊 Approach Comparison

| Approach | Time | Space | Note |
| :--- | :--- | :--- | :--- |
| **Re-sort every round** | $\mathcal{O}(n^2 \log n)$ | $\mathcal{O}(n)$ | Simple, but wasteful |
| **Max-heap via negation** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | General and optimal |
| **Counting array** | $\mathcal{O}(n + W)$ | $\mathcal{O}(W)$ | Only wins when max weight $W$ is small |

Each stone causes at most one push and two pops, and every heap operation is $\mathcal{O}(\log n)$.

---

### 🎯 Key Takeaway

When a problem keeps asking for "the current max (or min), then update," think priority queue. When your heap only offers min, negate numeric keys. For arbitrary objects, wrap them with a custom `__lt__`, at the cost of extra allocations and slower comparisons. On 3.14+, reach for the built-in max-heap functions instead.

What's your go-to trick when a standard library gives you the wrong kind of heap? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #LeetCode #SoftwareEngineering #CodingInterview #CleanCode
