
<div align = "center">

<img src = "assets/repoScanner_logo.png" alt = "repoScanner logo">

<a href = "LICENSE.md">
<img src = "https://img.shields.io/badge/license-MIT-1a1a1a?style=flat-square" alt = "License: MIT"></a>
<a href = "https://www.python.org/downloads/">
<img src = "https://img.shields.io/badge/python-3.12+-1a1a1a?style=flat-square&logo=python&logoColor=888888" alt = "Python: 3.12+"></a>
<a href = "https://github.com/tecnolgd/repoScanner">
<img src = "https://img.shields.io/badge/interface-CLI-1a1a1a?style=flat-square" alt = "Interface: CLI"></a>
<a href = "https://github.com/tecnolgd/repoScanner/releases">
<img src="https://img.shields.io/github/v/release/tecnolgd/repoScanner?include_prereleases&color=1a1a1a&style=flat-square" alt="Version"></a>
<a href = "#documentation">
<img src = "https://img.shields.io/badge/docs-available-1a1a1a?style=flat-square" alt = "Docs: Available"></a>
<a href = "https://github.com/tecnolgd/libcvault"><img src = "https://img.shields.io/badge/submodule-libcvault-1a1a1a?style=flat-square" alt = "Submodule: libcvault"></a>

</div>

---
<p align = "center">repoScanner is a lightweight repository analysis tool for developers.</p>          

> - Quickly understand your codebase structure, dependencies, and metrics with a single command.
> - Built for developers with the intent of saving time and peace-of-mind

## What It Does

- **Directory Analysis**: Scan total files, lines of code, average file size, and directory structure.
- **Dependency Detection**: Extract Python imports and C/C++ includes for each file.
- **Language Breakdown**: Group files by recognized language or extension.
- **Summary and Raw Reporting**: Choose a compact summary or detailed file-by-file dependency output.
- **JSON Export**: Generate a machine-readable report for every scan invocation.
- **Native File Utilities**: Optional `vendor/libcvault` support accelerates directory scanning, file sorting, search, byte totals, and line counts.
- **Transparent Fallback**: When the native helper is unavailable, repoScanner uses Python's `os.walk` and standard-library utilities.

## Current Version

The current development version is **0.3.0b10.dev26**, generated from the repository's Git history. The package metadata declares the release line as `0.3.0b10` with a development suffix.

## Features

### Reporting Modes

- **Stats mode** (default): High-level repository summary.
- **Raw mode** (`--raw` or `--dev`): Detailed, file-by-file dependency output.
- **Nerd mode** (`--nerd`): Alias for stats mode.

### Key Metrics

- Total files, bytes, and lines of code.
- Average file size and average lines per file.
- Largest files by line count and by byte size.
- Dependency totals, most-dependent file, and average dependencies per file.
- Language distribution by extension.
- Directory counts, extension counts, and maximum path depth.

### Runtime Dependencies

- The normal Python runtime uses only the Python Standard Library.
- The optional native helper is bundled as the `vendor/libcvault` submodule.
- `repoScan/scanner/libcvault_wrapper.py` loads the helper once per root path and caches the scan result.
- The native helper is not required for the core scan, summary, raw, or JSON-report commands.
- Building the helper requires a C++ compiler, Python development headers, and `pybind11`.

## Benchmarks

> These numbers are obtained by testing the commands using [**hyperfine**](https://github.com/sharkdp/hyperfine) on my own repository called [velocache](https://github.com/tecnolgd/velocache).


### Modes using libcvault

| Operation | Command | Mean (ms) | Std Dev (ms) | Range (ms) | Runs |
|---|---|---:|---:|---|---:|
| stats | `python3 -m repoScan.cli --stats` | 49.9 | 3.3 | 43.9-62.9 | 54 |
| dev | `python3 -m repoScan.cli --dev` | 48.9 | 2.6 | 42.4-54.6 | 53 |  
| search | `python3 -m repoScan.cli --search src/cache.cpp` | 58.1 | 2.8 | 53.1-66.4 | 46 |
| total bytes | `python3 -m repoScan.cli --tbytes` | 56.8 | 2.1 | 52.9-61.6 | 50 |
| sort(size-based) | `python3 -m repoScan.cli --sort` | 48.8 | 3.2 | 43.7-56.3 | 58 |
| max file size| `python3 -m repoScan.cli --max` | 56.7 | 2.5 | 52.9-67.6 | 50 |
| file line count | `python3 -m repoScan.cli --lc src/cache.cpp` | 55.6 | 1.7 | 52.8-60.7 | 50 |

### Direct Python vs. Shell Wrapper(reposcan)         

| Mode | Direct Python(ms) | Shell Wrapper(ms) | Shell overhead(ms) |
| :--: | :--: | :--: | :--: |
| stats | 49.9 | 56.5 | ~6.6 |
| dev | 48.9 | 56.4 | ~7.5 |


> [!TIP]     
> For reproducing benchmarks, check [benchmarking using hyperfine](assets/docs/testing.md#reproducing-benchmarks).


## Requirements

- Python 3.12+ (tested on Ubuntu 24.04 LTS)

    > The code uses only Python standard libraries and should be compatible with Python 3.10+,
    > but has been officially tested on Python 3.12.

## Quick Install

Install directly from PyPI for end users:

```bash
pip install repoScanner
```

Run:
```bash
reposcan <path> [--stats|--raw|--dev|--nerd|--sort|--max|--search <filename>|--lc <filename>|--tbytes|--help|--bench]
```

The scan and utility commands use the same argument parser. Options may appear before or after the path. The `--bench` command runs the bundled benchmark suite instead of scanning a repository.

```bash
reposcan <path> --stats
reposcan <path> --raw
reposcan <path> --dev                 # alias for --raw
reposcan <path> --nerd                # alias for --stats
reposcan <path> --sort                # files sorted by byte size
reposcan <path> --max                 # largest file and its byte size
reposcan <path> --search <filename>   # matching file name and its byte size
reposcan <path> --lc <filename>       # line count for a file
reposcan <path> --tbytes              # total bytes for the scanned tree
reposcan <path> --help                # show CLI help
```

Every normal scan or utility invocation also writes `output/report.json`. The benchmark command does not write this report. The native `libcvault` implementation sorts files by byte size in ascending order, while the Python fallback currently sorts them in descending order.

## Build Instructions

### 1. Setup

- Clone the repository

    ```bash
    git clone https://github.com/tecnolgd/repoScanner.git
    ```
- Navigate to the directory

    ```bash
    cd repoScanner
    ```
- **Optional**: Fetch bundled native helper(`libcvault`)

     ```bash
    git submodule update --init --recursive vendor/libcvault
    ```
    - `git submodule init` registers the submodule in your local repo configuration.
    - `git submodule update --init` also clones and checks out the correct commit for the submodule.        

> [!TIP]          
> If you later want to refresh `libcvault` from its remote repository, run:       
>
>   ```bash
>    git submodule update --remote vendor/libcvault
>    ```
>
> - This updates the submodule to the latest commit from its configured branch. You should then review and commit the updated submodule pointer in the main repo.
>
> Build the native extension from `bridge.cpp` and `vendor/libcvault/main.cpp`.
>
> - Before building, make sure system dev packages and `pybind11` are available. Debian/Ubuntu example:
>
>   ```bash
>   sudo apt-get update
>   sudo apt-get install -y build-essential g++ python3-dev
>   python3 -m pip install --user pybind11
>   ```
>
> - Compile using `pybind11` includes for portability:
>
>   ```bash
>   g++ -O3 -shared -std=c++17 -fPIC $(python3 -m pybind11 --includes) -I vendor/libcvault vendor/bridge.cpp vendor/libcvault/main.cpp -o repoScan/libcvault$(python3-config --extension-suffix)
>   ```


> [!IMPORTANT]
> 1. The `vendor/libcvault` native helper uses a pybind11 bridge for optimized filesystem operations.
> 2. Building the helper requires a C++ compiler (for example, `g++`), Python development headers, and `pybind11`.
> 3. The helper is optional. The Python fallback keeps the core commands working without it.
> 4. The submodule is tracked by `.gitmodules`; do not exclude `vendor/` from version control if the native helper must remain reproducible.

The repository may contain a prebuilt binary such as `libcvault.cpython-312-x86_64-linux-gnu.so`. Distribution packages should prefer wheels for the target platforms rather than committing platform-specific `.so` files.


### 2. Tool Execution/Run

The easiest way to use repoScanner is with the provided shell script wrapper:

```bash
./reposcan <path> [--stats|--raw|--dev|--nerd|--sort|--max|--search <filename>|--lc <filename>|--tbytes|--help|--bench]
```

**Quick start:**

```bash
./reposcan .                       # stats mode
./reposcan /path/to/repo --raw     # detailed developer output
./reposcan /path/to/repo --bench   # benchmark harness
./reposcan /path/to/repo --sort    # files sorted by byte size, largest first
```

### 3. Output

- Terminal output is printed according to the selected mode.
- A JSON report is always written to `output/report.json` for normal scans and utility commands.
- The JSON report contains the UTC generation timestamp and the normalized metrics returned by `generate_metrics`.
- The output directory is created automatically when needed.

## Supported Languages

Detects and maps **40+ extensions** to human-readable names, including:
* **Systems:** C, C++, Rust, Go, Zig, Swift
* **Web:** HTML, CSS, JavaScript, TypeScript, PHP
* **Data:** JSON, YAML, TOML, SQL, XML
* **Scripting:** Python, Ruby, Lua, Shell, PowerShell and many more. 
*(Unrecognized extensions fall back to their raw string format).*

## Documentation
* [Architecture](assets/docs/architecture.md)
* [Usage](assets/docs/usage.md)
* [Testing](assets/docs/testing.md)
* [Roadmap](assets/docs/roadmap.md)

## [Contributing](CONTRIBUTING.md)

## Contributors

A huge thanks to the developers contributing to repoScanner.
- [@Ghraven](https://github.com/Ghraven)
- [@AzarAI-TOP](https://github.com/AzarAI-TOP)
- [@Benjamin Ayiovh](https://github.com/BenjaminAyivoh1)
- [@faizan-7890](https://github.com/faizan-7890)

## License   
MIT