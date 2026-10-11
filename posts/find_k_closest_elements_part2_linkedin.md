# From Scanning a Million Elements to Looking at About Twenty 🔍

In Part 1, a heap solved Find K Closest Elements correctly but never used the fact that the array is **sorted**. Here's what that guarantee buys you.

---

### 💡 The Key Insight

In a sorted array, the $k$ closest elements to $x$ always form a **contiguous window**. So the problem isn't "pick $k$ elements." It's "find where the window starts."

---

### 🔧 Binary Search on the Window, Not on the Value

Candidate window starts range from $0$ to $n - k$. For a candidate start `mid`, the window is `arr[mid .. mid+k-1]`. Compare its two competing edges:

- the **leftmost** element in the window, `arr[mid]`
- the first element **just outside** it on the right, `arr[mid + k]`

If the left edge is *farther* from $x$ than the outside element, the window should slide right, so discard `mid` and everything before it. Otherwise the window can stay, or move left, so keep `mid` as a candidate.

On an exact tie we keep the left side, which gives the "prefer the smaller element" rule for free.

Then slice out $k$ elements from the final start.

---

### 📊 Complexity

| | Heap | Binary Search |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(n \log k)$ | $\mathcal{O}(\log(n-k) + k)$ |
| **Extra space** | $\mathcal{O}(k)$ | $\mathcal{O}(1)$ beyond the output |
| **Needs sorted input** | No | Yes |

The $+k$ is just copying the answer out. The search itself touches only $\mathcal{O}(\log n)$ elements.

---

### ⏱️ The Measured Difference

Sorted random arrays, best of three:

| $n$ | $k$ | Heap | Binary search |
| :--- | :--- | :--- | :--- |
| 100,000 | 10 | 21 ms | 2.5 µs |
| 1,000,000 | 10 | 427 ms | 4.4 µs |
| 1,000,000 | 1,000 | 604 ms | 14 µs |
| 1,000,000 | 100,000 | 996 ms | 1.4 ms |

Both always returned identical answers. When $k$ is small, that's **five orders of magnitude**. When $k$ is large, the gap narrows because copying the output starts to dominate, which matches the complexity.

---

### ⚠️ The Trade-off

The binary search is only valid if the input really is sorted. The heap version still works on unsorted data, so it's the safer choice if that guarantee ever weakens. I added explicit handling for $k \le 0$ and $k \ge n$ so the search never indexes out of range.

---

### 🎯 Key Takeaway

When a problem hands you sorted input, ask whether the answer has *shape*, such as a window, a prefix or a boundary. If so, search for the shape instead of examining the elements.

What's the biggest speedup you've gotten by finally using a guarantee you'd overlooked? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #BinarySearch #SlidingWindow #BigO #LeetCode #SoftwareEngineering #CodingInterview
