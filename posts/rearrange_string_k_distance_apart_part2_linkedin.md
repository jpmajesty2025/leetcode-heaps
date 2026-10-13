# Array Scans vs. Heap Queues: Benchmarking Cooldown Systems (Part 2 of 2) 🚀

In Part 1, we introduced the Max-Heap + FIFO Cooldown Deque pattern to place identical characters at least distance $k$ apart.

Since English lowercase letters only have 26 characters ($|Σ| \le 26$), many developers wonder:
*Why bother with a heap and a deque when you can just scan a 26-element array?*

Let's test that hypothesis.

---

### 🧱 The Direct Frequency Table Alternative

Instead of queues, you can maintain:
1️⃣ An array of remaining counts: `counts = [0] * 26`
2️⃣ An array of last seen positions: `last_pos = [-k] * 26`

At each position from $0$ to $n - 1$:
- Loop through all 26 characters
- Find the valid character with the maximum count whose cooldown has elapsed (`pos - last_pos[c] >= k`)
- Place it, decrement its count, and update `last_pos[c]`

It uses simple arrays with no heap allocations. But how fast is it really?

---

### 😬 Then I Benchmarked Them (50,000 Characters)

I ran both approaches on a 50,000-character workload with $k = 3$:

| Implementation | Runtime (50k chars) | Time Complexity | Winner |
| :--- | :--- | :--- | :--- |
| **Frequency Table Scan** | 53.07ms | O(n · |Σ|) | 2x Slower |
| **Max-Heap + Deque** | **26.07ms** | **O(n log |Σ|)** | **Heap (2.04x faster!)** |

Even with just 26 characters, the **Max-Heap + Deque is over 2x faster**!

---

### 🔍 Why the Heap + Deque Wins

1️⃣ **Eliminating Redundant Scans**:
The table scan evaluates all 26 characters at every single position:
$50{,}000 \times 26 = 1{,}300{,}000$ loop checks!
The heap only tracks *active, eligible* characters.

2️⃣ **O(1) Cooldown Transitions**:
The FIFO deque buffers characters in exact arrival order. Releasing an expired character is a simple `popleft()` in O(1) time.

3️⃣ **Scalability to Large Alphabets**:
If you process Unicode, byte tokens, or distribute tasks across 10,000 worker IDs, the array scan degrades to a brutal O(n · |Σ|). The heap and deque scale effortlessly at **O(n log |Σ|)**.

---

### 🧪 How I Verified It

I tested both implementations with a 31-test suite and Hypothesis property-based testing:
- **Anagram Preservation**: Result is an exact multiset permutation of input $s$
- **Distance Verification**: Every identical character pair is strictly $\ge k$ indices apart
- **100% Consensus**: Both solutions agree on feasibility across arbitrary random inputs

---

### 🎯 Key Takeaway

Don't let small constants trick you into linear scans. A Max-Heap paired with a sliding FIFO deque isolates eligible resources and eliminates millions of wasteful checks.

Where else in your systems do you use sliding cooldown buffers? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #SystemDesign #Benchmarking #LeetCode #SoftwareEngineering #CodingInterview
