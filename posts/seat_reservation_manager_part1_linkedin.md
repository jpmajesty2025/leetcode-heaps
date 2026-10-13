# The Hidden O(n²) Trap in System Design (Part 1 of 2) 🎟️

**The Problem**:
Design a `SeatManager` class that dynamically manages $n$ seats numbered from $1$ to $n$.
- `reserve()`: Fetches the smallest-numbered unreserved seat, marks it reserved, and returns it.
- `unreserve(seatNumber)`: Releases the seat back to the pool of available seats.

It sounds simple enough. But an innocent-looking implementation can bring down an entire service.

---

### ⚠️ The Naive Disaster

Here is the most common pitfall when developers prototype this with a list:
- Start with `available = [1, 2, ..., n]`
- On `reserve()`: call `available.pop(0)` to grab the smallest seat
- On `unreserve(seat)`: append `seat` and call `available.sort()`

Why is this disastrous?
1️⃣ `pop(0)` is an **O(n)** operation. It shifts every remaining seat to the left in memory via `memmove`.
2️⃣ Calling `available.sort()` on every release costs **O(n log n)**.

Across $100{,}000$ operations on $100{,}000$ seats, this triggers billions of operations—resulting in an instant Time Limit Exceeded (TLE) and massive latency spikes.

---

### 🔧 The Textbook Fix: A Min-Heap

The operation we need is: *repeatedly fetch the minimum available number, and insert released numbers efficiently.*

That is the textbook definition of a **Priority Queue (Min-Heap)**:
- Pre-populate all $n$ seats into a list `[1, ..., n]`
- Run `heapify` at initialization in O(n) time
- `reserve()`: extract the root with `heappop` in **O(log n)**
- `unreserve()`: push the seat with `heappush` in **O(log n)**

Now, both operations run in logarithmic time regardless of list size!

---

### 📊 Complexity Comparison

- **Naive List:** O(n) reserve, O(n log n) unreserve
- **Full Min-Heap:** O(log n) reserve, O(log n) unreserve, O(n) space

---

### 🤔 But Can We Do Better?

The full min-heap passes LeetCode. But think about real systems:
- If a stadium has $100{,}000$ seats, why pre-allocate $100{,}000$ integers upfront before a single fan buys a ticket?
- What if $n = 10^9$? Pre-allocating the heap causes an immediate `MemoryError`!

In Part 2, we'll see how a lazy pointer pattern achieves **O(1) initialization** and **1,000x faster startup**.

Have you ever seen an accidental `pop(0)` bottleneck in production? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #SystemDesign #LeetCode #SoftwareEngineering #CodingInterview
