# Finding Closest Points with a MAX-Heap (And Why √(x²+y²) is a Trap) (Part 1 of 2) 🎯

**The Problem**:
Given an array of points on the X-Y plane and an integer $k$, return the $k$ points closest to the origin $(0, 0)$. You may return the answer in any order.

---

### ⚠️ Trap 1: The Square Root Trap

The mathematical formula for Euclidean distance is $\sqrt{x^2 + y^2}$.

Taking the square root introduces floating-point arithmetic, precision loss, and unnecessary CPU overhead. Because $f(d) = d^2$ is strictly monotonic for non-negative distances, we can compare squared distances directly:
$x_1^2 + y_1^2 < x_2^2 + y_2^2$

In Python, computing `x * x + y * y` is roughly 25-30% faster than `x ** 2 + y ** 2` because integer multiplication bypasses general power routines.

---

### 🤔 Trap 2: Why "Closest" Needs a MAX-Heap

When searching for the closest points, intuition tempts you to reach for a min-heap. But what you actually need is a **max-heap bounded at size $k$**:

1️⃣ Keep a pool of the $k$ best candidates seen so far
2️⃣ The root of the max-heap holds the **farthest** point among those $k$ candidates
3️⃣ When a new point arrives, compare it against the root. If it's closer, evict the root and insert the newcomer
4️⃣ After inspecting all points, the heap holds the $k$ closest points

A min-heap puts the closest point at the root—the one value you never want to throw away! A max-heap exposes the weakest survivor, making eviction effortless.

Since Python's `heapq` is natively a min-heap, negating the squared distance `(-dist, point)` flips the priority, turning the farthest point into the root.

---

### ⚡ The Power of `heapreplace` Filtering

Seed the heap with the first $k$ points using O(k) `heapify`.

For the remaining $n - k$ points, only touch the heap when the new point is strictly closer than the root. With `heapreplace`, eviction and insertion happen in a single downward sift.

In large inputs, the root distance tightens rapidly. Over 99% of subsequent points are rejected immediately with a single O(1) integer comparison without touching the heap!

---

### 📊 Complexity

- **Time:** O(n log k)
- **Space:** O(k) auxiliary space

---

### 🎯 Key Takeaway

Compare squared distances to stay in integer space, and use a bounded max-heap to evict the farthest candidates. But can we eliminate the log k factor entirely? We'll see how Quickselect compares in Part 2.

Did you fall into the square root trap the first time you solved this? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #LeetCode #SoftwareEngineering #CodingInterview
