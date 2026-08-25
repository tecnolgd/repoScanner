# Benchmarking

This project includes both script-based benchmark suite as well as precision performance profiling benchmarks.


## Reproducing benchmarks

- **Quick Synthetic Benchmark**

    - Open the terminal and run:
        ```bash
        python3 tests/benchmark.py #or ./reposcan --bench
        ```
    - Sample Output    

        ```txt
        [✓] Pre-allocating mock codebase in 'tests/perf_test_sandbox' with 2500 files...

        [✓] Launching tool environment execution...

        ==================================================
                repoScanner Benchmark Suite
        ==================================================
         Target Workspace        : tests/perf_test_sandbox
         Total Files Processed   : 2500
         Execution Time          : 0.24334 seconds
         I/O Processing Velocity : 10273.71 files/sec
        ==================================================
        [✓] Flushed test sandbox environment directories cleanly. 
        ```

- **Precision Performance Profiling**     
      
    > Requires `hyperfine 1.18.0` and above.

    - Run individual benchmark modes:
        ```bash
        # Standard stats & dev boot
        hyperfine 'python3 -m repoScan.cli <path> --stats'
        hyperfine 'python3 -m repoScan.cli <path> --dev'

        # Feature modes
        hyperfine 'python3 -m repoScan.cli <path> --sort'
        hyperfine 'python3 -m repoScan.cli <path> --lc'
        hyperfine 'python3 -m repoScan.cli <path> --max'
        hyperfine 'python3 -m repoScan.cli <path> --tbytes'
        hyperfine 'python3 -m repoScan.cli <path> --search <filename>'
        ```

    - Sample output(tested on `velocache`)         

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


## Test guidance

- Add unit tests or sample scenarios under `tests/`.
- Keep tests small and repeatable.
- When adding new analyzers or CLI features, verify both normal and edge-case scanning behavior.

