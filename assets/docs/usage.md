# Usage guide

Use repoScanner to analyze a repository/directory from the command line.

## Quick start

### Using shell wrapper

```bash
./reposcan /path/to/repo [--stats|--raw|--dev|--bench]
```

Cases:

```bash
./reposcan .                                 # scan current directory in summary mode
./reposcan /path/to/repo --stats             # explicit stats mode
./reposcan /path/to/repo --raw               # or '--dev'(alias)   # detailed file-by-file dependency analysis
./reposcan --bench                           # run benchmark harness
./reposcan --help  #or -h                    # shows available CLI options.

# Additional Modes
./reposcan /path/to/repo --max               # return largest file
./reposcan /path/to/repo --tbytes            # returns total size of the directory(in bytes)
./reposcan /path/to/repo --sort              # sorts files in ascending order
./reposcan /path/to/repo --lc <filename>     # returns line count of a given file
./reposcan /path/to/repo --search <filename> # search a given file
```

## Direct python execution

```bash
python3 -m repoScan.cli /path/to/repo [--stats|--raw|--dev|--help]
```

> [!IMPORTANT]
> If [libcvault](https://github.com/tecnolgd/libcvault) is available, repoScanner will use it for directory scanning, optional utility commands such as sorting, searching, and byte totals. If it is missing, the same commands continue to work through the built-in Python fallback.


> [!TIP]      
> Check [libcvault API reference](https://github.com/tecnolgd/libcvault/blob/main/docs/reference.md#3-api-reference) for more details.

## Output

- `output/report.json` is the default JSON report output file.
- Terminal output summarizes key metrics and execution status.

> [!NOTE]       
> - `--stats` is the default mode when no mode is specified.
> - `--raw` and `--dev` both produce the detailed dependency tree output.
> - `--bench` runs the bundled benchmark harness implemented in `tests/benchmark.py`.- Scans are cached per root path, so repeated calls for the same directory reuse the existing scan results instead of rescanning the tree unnecessarily.
