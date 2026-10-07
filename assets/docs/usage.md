# Usage guide

Use repoScanner to analyze a repository/directory from the command line.

## Quick start

### Using the shell wrapper

```bash
./reposcan /path/to/repo [options]
```

The path can be placed before or after an option. The default mode is `--stats`.

```bash
./reposcan .                              # summary mode
./reposcan /path/to/repo --stats          # explicit summary mode
./reposcan /path/to/repo --raw            # detailed dependency output
./reposcan /path/to/repo --dev            # alias for --raw
./reposcan /path/to/repo --nerd           # alias for --stats
./reposcan --bench                        # run the benchmark harness
./reposcan --help                         # show the wrapper help
```

### Additional utility modes

```bash
./reposcan /path/to/repo --sort           # files sorted by byte size
./reposcan /path/to/repo --max            # largest file and its byte size
./reposcan /path/to/repo --search filename # file name and byte size
./reposcan /path/to/repo --lc filename    # line count for the file
./reposcan /path/to/repo --tbytes         # total bytes in the tree
```

`--search` and `--lc` require a filename argument. The wrapper reports an error when the argument is missing. The native `libcvault` implementation sorts files by byte size in ascending order, while the Python fallback currently sorts them in descending order.

## Direct Python execution

```bash
python3 -m repoScan.cli /path/to/repo [--stats|--raw|--dev|--nerd|--sort|--max|--search <filename>|--lc <filename>|--tbytes|--help]
```

The command accepts the same modes as the wrapper and saves the report to `output/report.json` after each normal invocation.

> [!IMPORTANT]
> When [libcvault](https://github.com/tecnolgd/libcvault) is available, repoScanner uses it for directory scanning and the optimized utility commands. If it is unavailable, the same commands use the built-in Python fallback.

> [!TIP]
> See the [libcvault API reference](https://github.com/tecnolgd/libcvault/blob/main/docs/reference.md#3-api-reference) for the native helper interface.

## Output

- `output/report.json` is the default JSON report path.
- The report contains a UTC `generated_at` timestamp and the current metrics object.
- Terminal output reflects the selected mode.
- The JSON report is generated after every normal scan or utility command; `--bench` is the exception.
- Directory scans are cached by absolute root path, so repeated scans of the same directory avoid another traversal when the process remains alive.

## JSON report structure

```json
{
  "generated_at": "2026-10-06T12:00:00",
  "metrics": {
    "file_metrics": {
      "total": 0,
      "total_bytes": 0,
      "total_lines": 0,
      "average_lines": 0,
      "average_file_size": 0,
      "largest_file": null,
      "max_file": null
    },
    "dependency_metrics": {
      "total": 0,
      "max_file": null,
      "average": 0
    },
    "language_metrics": {}
  }
}
```

The analyzer-specific intermediate results are not serialized directly; the report exposes the normalized metrics produced by `generate_metrics`.
