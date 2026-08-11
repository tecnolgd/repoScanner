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

        [✓] Launching tool environment execution via ./reposcan wrapper...

        ==================================================
            repoScanner Benchmark Suite            
        ==================================================
        Target Workspace        : tests/perf_test_sandbox
        Total Files Processed   : 2500
        Execution Time          : 0.36267 seconds
        I/O Processing Velocity : 6893.38 files/sec
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

    - Sample outputs     
    
        - `hyperfine 'python3 -m repoScan.cli --stats'`

            ```txt
            Benchmark 1: python3 -m repoScan.cli --stats
            Time (mean ± σ):     122.9 ms ±  13.9 ms    [User: 70.3 ms, System: 63.2 ms]
            Range (min … max):   102.8 ms … 151.2 ms    22 runs
            ```

        - `hyperfine 'python3 -m repoScan.cli --dev`    

            ```txt
            Benchmark 1: python3 -m repoScan.cli --dev
            Time (mean ± σ):     127.8 ms ±  22.8 ms    [User: 72.7 ms, System: 66.3 ms]
            Range (min … max):   106.8 ms … 208.0 ms    20 runs
            ```


## Test guidance

- Add unit tests or sample scenarios under `tests/`.
- Keep tests small and repeatable.
- When adding new analyzers or CLI features, verify both normal and edge-case scanning behavior.

