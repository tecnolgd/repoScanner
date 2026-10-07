# Testing and benchmarking

This project includes a pytest suite and a script-based benchmark harness. The benchmark results are environment-dependent and are not a substitute for automated regression tests.

## Running the test suite

```bash
pytest
```

Run a single test file or test during development:

```bash
pytest tests/test_core.py
pytest tests/test_core.py::test_dir_scanner_list
```

The current tests cover Python and C/C++ dependency extraction, size and structure analysis, directory scanning, and metrics aggregation.

## Reproducing benchmarks

### Quick synthetic benchmark

Run either command:

```bash
python3 tests/benchmark.py
./reposcan --bench
```

The harness creates a temporary synthetic repository, runs the scanner's benchmark modes, and removes the temporary directory afterward.

### Precision performance profiling

> Requires `hyperfine` 1.18.0 or newer.

Run individual benchmark modes with the required filename argument where applicable:

```bash
hyperfine 'python3 -m repoScan.cli <path> --stats'
hyperfine 'python3 -m repoScan.cli <path> --dev'
hyperfine 'python3 -m repoScan.cli <path> --sort'
hyperfine 'python3 -m repoScan.cli <path> --lc <filename>'
hyperfine 'python3 -m repoScan.cli <path> --max'
hyperfine 'python3 -m repoScan.cli <path> --tbytes'
hyperfine 'python3 -m repoScan.cli <path> --search <filename>'
```

### Sample output
(Numbers obtained from profiling **tecnolgd/velocache**)

```txt
Benchmark 1: ./reposcan ~projects/velocache --stats
Time (mean ± σ):      56.5 ms ±   3.7 ms    [User: 37.9 ms, System: 23.6 ms]
Range (min … max):    50.5 ms …  73.3 ms    49 runs
```

```txt
Benchmark 1: ./reposcan ~projects/velocache --dev
Time (mean ± σ):      56.4 ms ±   3.3 ms    [User: 36.7 ms, System: 24.5 ms]
Range (min … max):    50.2 ms …  65.2 ms    47 runs
```

These figures are examples from the project's own benchmark environment and should not be treated as guaranteed results for every machine.

## Test Guidelines

- Add unit tests or sample scenarios under `tests/`.
- Name test functions with the `test_` prefix so pytest discovers them.
- Keep tests small, deterministic, and repeatable.
- When adding analyzers or CLI features, verify normal, empty, missing-path, and native-fallback scenarios where applicable.

