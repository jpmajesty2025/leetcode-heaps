# A Correct Heap Solution That Ignores the Best Clue in the Problem 🎯

**The Problem**:
Given a **sorted** integer array `arr` and integers $k$ and $x$, return the $k$ integers closest to $x$, sorted ascending. If two are equally close, prefer the smaller one.

---

### 🔧 The Heap Approach

Keep a heap of the $k$ best candidates seen so far, and evict the worst one whenever it grows past $k$:

1️⃣ For each number, compute its distance to $x$
2️⃣ Push `(-distance, -number)` onto Python's min-heap
3️⃣ If the heap exceeds $k$, pop. The root is the **farthest** candidate, so it's the one evicted
4️⃣ Sort what's left

---

### 🧠 The Detail That Makes It Correct

Python's heap is a min-heap, so negating the distance turns it into "farthest at the root." The second key matters just as much. On a distance tie, the root is the entry with the smallest `-number`, which is the **largest** number. So it's the larger of two equally-close elements that gets evicted, and the smaller one survives. That is exactly the tie-break the problem asks for.

Edge cases hold up too: $k = 0$ returns an empty list, $k$ larger than the array returns everything, and duplicates behave like any other values.

---

### 📊 Complexity

- **Time:** $\mathcal{O}(n \log k + k \log k)$
- **Space:** $\mathcal{O}(k)$

---

### 🤔 So What's Wrong With It?

Technically, nothing! But it **ignores** valuable information: the input is *sorted*. This solution works identically on a shuffled array, which means it's paying $\mathcal{O}(n)$ to examine every element when the structure of the data says most of them can't possibly matter. A solution that doesn't use a given guarantee is usually leaving performance behind.

We'll see how much in Part 2.

---

### 🎯 Key Takeaway

Before you ship, ask: be sure your solution fully exploits any guarantees in the problem statement. If you have not done so, you are leaving a more performant algorithm on the table.

Do you check for unused constraints before you code? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #LeetCode #SoftwareEngineering #CodingInterview
