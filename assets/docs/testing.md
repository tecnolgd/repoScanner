# Benchmarking

This project uses **hyperfine** for benhcmarking.

## Reproducing benchmarks

> [!IMPORTANT]    
> Requires hyperfine 1.18.0 and above.

- Mode based testing     

    1. Open the terminal and run
        ```bash
        hyperfine 'command'
        ```
        where command:      
        - `python3 -m repoScan.cli <path> [--stats|--dev]`      
        - `./reposcan <path> [--stats|--dev]`
            
            Mode based:      
            - `python3 -m repoScan.cli <path> --sort`    
            - `python3 -m repoScan.cli <path> --lc`     
            - `python3 -m repoScan.cli <path> --max`    
            - `python3 -m repoScan.cli <path> --tybtes` 
            - `python3 -m repoScan.cli <path> --search <filename>`

## Sample outputs

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

