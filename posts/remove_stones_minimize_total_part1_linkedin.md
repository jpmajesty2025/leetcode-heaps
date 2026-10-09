# The Bug That Passed My Eye Test: Floor vs. Float in a Heap Problem (Part 1 of 2) 🪨

**The Problem**:
You're given piles of stones and a number $k$. In each of exactly $k$ operations, pick a pile and remove $\lfloor p/2 \rfloor$ stones from it. Return the minimum total stones left.

Greedy is the natural fit: **always shrink the largest pile**, since removing $\lfloor p/2 \rfloor$ is worth more the bigger $p$ is. The array changes after every step, so a **max-heap** is the right tool.

Note that we saw a similar problem before - finding the minimum number of operations to halve the sum of an array. Tempting to reuse the same shape? It may look right. It isn't.

---

### 🐛 The Bug

The prior problem halved the largest remaining number with true division. Floating point data is fine. But this problem says **remove the floor of half**, so a pile of 5 loses 2 and keeps **3**, not 2.5. No floats allowed!

Same shape, different rules. Be careful about blindly copy-pasting a pattern: you are also copying its assumptions and they may not all hold.

---

### 🔧 The Fix

A pile of $p$ loses $\lfloor p/2 \rfloor$, so it keeps $p - \lfloor p/2 \rfloor = \lceil p/2 \rceil$. That's integer arithmetic.

1️⃣ Heapify the negated piles in $\mathcal{O}(n)$ (`heapq` is min-only before 3.14)
2️⃣ Pop the largest, push back $\lceil p/2 \rceil$
3️⃣ Stop early if all piles are size 1 and you have not expended $k$ operations, because $\lfloor 1/2 \rfloor = 0$ and nothing can shrink further
4️⃣ Sum what's left

---

### 📊 Complexity

- **Time:** $\mathcal{O}(n + k \log n)$
- **Space:** $\mathcal{O}(n)$

---

### 🎯 Key Takeaway

Reusing a pattern is a good instinct. Reusing its **assumptions** without rereading the problem is how bugs sneak in. Floor, ceil and true division are three different operations.

Have you been bitten by a copy-pasted pattern that almost fit? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #Greedy #LeetCode #SoftwareEngineering #CodingInterview
