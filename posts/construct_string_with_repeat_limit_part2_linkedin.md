# Max-Heap vs. 26-Element Array: Alphabet Scaling Trade-offs (Part 2 of 2) ⚖️

In Part 1, we used a Max-Heap to greedily build repeat-limited strings with a 1-character delimiter rule.

Since the problem restricts inputs to lowercase English letters, can we eliminate heap overhead?

Yes—with a **26-Element Frequency Array and Two Pointers**.

---

### 🧱 The 26-Element Two-Pointer Pattern

English lowercase letters have 26 characters ($|Σ| = 26$):
1️⃣ Count frequencies in an array: `counts = [0] * 26`
2️⃣ Pointer `i = 25` (tracks largest available character, starting at 'z')
3️⃣ Pointer `j = 24` (scans down for the next delimiter)

While `i >= 0`:
- Append `use = min(counts[i], repeatLimit)` copies of character `i`
- If character `i` still has copies left, advance pointer `j` downward until finding the next non-zero bucket
- If no delimiter bucket exists, break! Otherwise, append one delimiter character, decrement `counts[j]`, and resume with `i`

No heapify, no tuple allocations, and no tree sifting.

---

### 😬 Then I Benchmarked Them (100,000 Characters)

| Implementation | Runtime (100k chars) | Time Complexity | Winner |
| :--- | :--- | :--- | :--- |
| **Max-Heap** | 22.40ms | O(n + |Σ| log |Σ|) | Fast |
| **26-Element Array** | **18.26ms** | **O(n + |Σ|)** | **Array (~1.2x faster)** |

The array avoids heap allocations and runs slightly faster. But is it always the right choice?

---

### 🔍 When Does the Heap Win? (Alphabet Scaling)

The array solution relies on a key assumption: **the alphabet size is tiny ($|Σ| = 26$).**

What happens if requirements change?
- **Full Unicode ($140{,}000+$ code points)**: Linearly scanning an array of size 140,000 for a delimiter costs O(|Σ|) per lookup.
- **Large Vocabularies or Token Streams**: Sparse arrays waste memory and degrade cache locality.

A **Max-Heap** only stores distinct characters that actually appear in the input ($m \le n$). Finding the delimiter is always **O(log m)**, scaling gracefully to arbitrary alphabets!

---

### 🧪 How I Verified It

I tested both implementations with a 29-test suite and Hypothesis:
- Verified repeat-limit invariant: no character streak exceeds `repeatLimit`
- Proved multiset conservation: output counts never exceed input counts
- 100% agreement between Heap and Array solutions across random strings

---

### 🎯 Key Takeaway

For small fixed alphabets ($|Σ| \le 26$), a two-pointer array is lightweight and fast. For arbitrary or Unicode alphabets, a Max-Heap provides generalized O(log m) performance that doesn't depend on universe size.

Do you prefer specializing algorithms to fixed alphabets or keeping them general with heaps? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #Greedy #Benchmarking #LeetCode #SoftwareEngineering #CodingInterview
