# Why Halving the Biggest Number Is Always the Right Move ✂️

**The Problem**:
You're given an array of positive integers. In one operation, you can pick any number and replace it with exactly half its value (and you may pick the same, already-halved number again later). Return the minimum number of operations needed to reduce the array's sum by at least half.

The instinct is greedy: **always halve the largest value**. The array changes after every step, which is the signal for a **max-heap**.

---

### 💡 Why Greedy Works

Halving a number $x$ removes exactly $x/2$ from the sum. So each operation's payoff is *half the value you pick*. To remove as much as possible per operation, always pick the current maximum.

An exchange argument backs this up: if an optimal plan halves a smaller value while a larger one is available, swapping them never removes less. Largest-first can't lose.

---

### 🔧 The Approach

1️⃣ **Track the sum**: compute the total once, then the target ($\text{total} / 2$).
2️⃣ **Heapify negatives**: `heapq` is a min-heap, so store negated values. Linear-time build at $\mathcal{O}(n)$.
3️⃣ **Pop, halve, push back**: each round removes half the largest value from the running sum and re-inserts the smaller remainder.
4️⃣ **Stop at the threshold**: loop while the running sum is still strictly above the target.

---

### ⚠️ The Subtle Part: Floats and Ties

"At least half" means an *exact tie counts*. Take five 1s: the sum is 5, the target is 2.5, and after five halvings the sum is exactly 2.5. The strict `>` comparison correctly stops there.

Floats can make you nervous here, but halving is **exact** in binary floating point (it only shifts the exponent). I still tested it: 100,000 copies of ten million, where the sum lands exactly on the target, plus random inputs against an oracle built on Python's `Fraction`.

---

### 📊 Complexity

- **Time:** $\mathcal{O}(n + k \log n)$ with $k \le n$, since halving every element once removes exactly half the sum. So $\mathcal{O}(n \log n)$ overall.
- **Space:** $\mathcal{O}(n)$ for the heap.

---

### 🧪 How I Trusted It

- A `Fraction`-based simulation as the exact oracle
- Exhaustive search over every sequence of choices on tiny arrays, an independent check that greedy is truly minimal
- Properties: order doesn't matter, the answer is between 1 and $n$, and scaling all values by a constant changes nothing

---

### 🎯 Key Takeaway

When each step's payoff depends on the current maximum, and the state changes after every step, reach for a max-heap. Then verify the greedy claim with brute force on small inputs instead of trusting intuition.

How do you validate a greedy solution before you commit to it? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #Greedy #LeetCode #SoftwareEngineering #CodingInterview
