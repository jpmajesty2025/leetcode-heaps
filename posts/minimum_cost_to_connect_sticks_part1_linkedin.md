# Huffman Coding in Disguise: Connecting Sticks with a Min-Heap (Part 1 of 2)🪵

**The Problem**:
You have sticks of various lengths. Connecting two sticks of lengths $x$ and $y$ costs $x + y$ and produces one stick of length $x + y$. Keep connecting until one stick remains. What's the minimum total cost?

The cost of a merge is the *size of the result*, and that result gets merged again later. So every stick is re-paid once for each merge above it. **Merge the short sticks first, so the repeated payments are made on small values and the long sticks are paid for as few times as possible.**

---

### 💡 The Greedy Rule

Always merge the **two shortest** sticks. This is exactly the construction behind **Huffman coding**: the same problem, wearing a different costume.

After each merge, the new stick joins the pool, so the paradigm is: "give me the two smallest, then insert a new value (the cost of merging the two)." That's a **min-heap**, and unlike earlier heap problems this time `heapq` fits natively, with no negation trick.

1️⃣ Heapify the sticks in $\mathcal{O}(n)$
2️⃣ Pop the two smallest and add their sum to the total
3️⃣ Push the merged stick back
4️⃣ Stop when one stick is left

---

### 🐛 The Quiet Side Effect I Found

My first version heapified the caller's list in place and popped from it. The answer was right, but after the call, `[2, 4, 3]` had become `[9]`. **The function destroyed its own input.**

The fix is one line: copy the list first. It's an easy thing to miss, because the result is correct and only the surrounding code pays for it.

---

### 📊 Complexity

- **Time:** $\mathcal{O}(n \log n)$. There are $n - 1$ merges, each with two pops and one push.
- **Space:** $\mathcal{O}(n)$

---

### 🎯 Key Takeaway

When the cost of an operation depends on the *size of its result*, and results keep getting reused, merge the smallest items first. And always check what your function does to its inputs.

What other problems have you recognized as Huffman in disguise? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #Greedy #Huffman #LeetCode #SoftwareEngineering #CodingInterview
