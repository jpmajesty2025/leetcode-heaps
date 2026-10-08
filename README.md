# leetcode-heaps

Practice implementations for LeetCode (and possibly other) heap problems, with tests written in `pytest` and `hypothesis`.

## Test structure

- Tests live under `tests/`
- File naming follows `test_<module>.py`
- Run all tests with:

```bash
pytest -q
```

## Property-based testing (Hypothesis)

Alongside example-based tests, this repo uses **property-based tests** with [Hypothesis](https://hypothesis.readthedocs.io/).

### Pattern used

1. Write a small **reference implementation** (oracle) that is simple and obviously correct.
2. Use Hypothesis strategies to generate many valid inputs.
3. Assert the real implementation matches the oracle and key invariants.