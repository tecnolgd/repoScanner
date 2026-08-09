# Testing

This project includes benchmark and automated test guidance to help verify repoScanner behavior.

## Benchmarking

To run the built-in benchmark harness:

```bash
python3 tests/benchmark.py
```

or:

```bash
./reposcan --bench
```

The benchmark suite creates a temporary sandbox directory, executes the CLI wrapper, and reports execution velocity along with cleanup status.

## Test data

Example and sample data for tests are available in:

- `assets/data/testData.txt`

Use these files to build deterministic test cases or validation scenarios.

## Test guidance

- Add unit tests or sample scenarios under `tests/`.
- Keep tests small and repeatable.
- When adding new analyzers or CLI features, verify both normal and edge-case scanning behavior.

## Notes

- The repository currently relies on the Python standard library, so tests should be runnable with the same Python interpreter used to run the tool.
- Benchmark execution should not depend on external network resources.
