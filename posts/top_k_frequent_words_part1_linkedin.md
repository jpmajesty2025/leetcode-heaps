# Why You Can't Negate a String: The Top-K Words Trap (Part 1 of 2) 🔡

**The Problem**:
Given an array of words and an integer $k$, return the $k$ most frequent words.
- Primary order: Frequency **descending** (higher frequency is better)
- Tie-breaker: Lexicographical order **ascending** (e.g. "i" beats "love")

LeetCode's follow-up challenges you: can you solve it in O(n log k) time and O(n) space?

---

### 🤔 The Counterintuitive Min-Heap Rule

To keep only $k$ elements in memory, use a **min-heap capped at size $k$**:

The root of the min-heap holds the **weakest** candidate in the top $k$, so it gets evicted whenever a stronger word arrives.

Who is the weakest candidate?
1️⃣ A word with **lower frequency** is weaker (should be evicted first).
2️⃣ On a frequency tie, the alphabetically **larger** word is weaker!
Between "apple" and "banana" appearing 3 times each, "apple" is preferred. So "banana" must be evicted first!

---

### 💥 The Python Trap: Strings Cannot Be Negated

In numeric heap problems, inverting priority is trivial: negate the number (`-distance`, `-val`).

In Python:
`-"apple"` ➡️ `TypeError: bad operand type for unary -: 'str'`

If you store standard `(freq, word)` tuples in a min-heap:
- Smaller frequency sits at the root (correct).
- But on ties, Python compares words alphabetically: "apple" < "banana".
- So "apple" sits at the root and gets evicted before "banana"! That's the **exact opposite** of what the problem requires.

---

### 🔧 The Solution: A Custom Comparator Class

Since we can't negate strings, we wrap entries in a lightweight class with a custom `__lt__`:
- Compare `freq` ascending (smaller frequency = smaller entry)
- Compare `word` **descending** (`self.word > other.word`), making alphabetically larger words smaller in the min-heap!

Now the min-heap evicts the right candidate on every tie. When done, popping from the heap yields words from weakest to strongest; reversing that list gives the exact required order!

---

### 📊 Complexity

- **Time:** O(n + m log k), where $n$ is total words and $m$ is distinct words
- **Space:** O(m + k) auxiliary space

---

### 🎯 Key Takeaway

When compound sorting requires opposite directions (one descending, one ascending) and one key cannot be negated, a custom comparator is the cleanest way to enforce exact eviction priority.

In Part 2, we'll see two alternative solutions that avoid custom classes entirely.

Have you ever hit the string negation limitation in Python? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #TopK #LeetCode #SoftwareEngineering #CodingInterview
