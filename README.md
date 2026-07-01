
<div align = "center">
<img src = "assets/repoScanner_logo.png" alt = "repoScanner logo">

<a href = "https://opensource.org/licenses/MIT"><img src = "https://img.shields.io/badge/License-MIT-green.svg" alt = "License: MIT"></a>
<a href = "https://www.python.org/downloads/"><img src = "https://img.shields.io/badge/Python-3.12%2B-blue" alt = "Python 3.7+"></a>
<img src = "https://img.shields.io/badge/interface-CLI-white">
<a href="https://github.com/tecnolgd/repoScanner/releases"><img src="https://img.shields.io/github/v/release/tecnolgd/repoScanner?include_prereleases&t=TIMESTAMP" alt="Release">
</a>
<a href="https://github.com/tecnolgd/repoScanner/graphs/contributors">
<img src="https://img.shields.io/github/contributors/tecnolgd/repoScanner?style=flat&color=orange" alt="Contributors Badge">
</a>
<a href = "#documentation"><img src = "https://img.shields.io/badge/docs-minimal-pink" alt = "Docs: Minimal"></a>
</div>

>**repoScanner** is a lightweight repository analysis tool for developers.          
>- Quickly understand your codebase structure, dependencies, and metrics with a single command.
>- Built for developers with the intent of saving time and peace-of-mind

## What It Does

- **File Analysis**: Scan total files, lines of code, and average file size
- **Dependency Detection**: Extract and map dependencies (Python imports, C/C++ includes)
- **Language Breakdown**: See what languages dominate your repo
- **Smart Reporting**: Choose between quick stats or detailed developer mode
- **JSON Export**: Machine-readable reports for automation

## Features

**Dual Reporting Modes**
- **Stats Mode** (default): High-level summary—perfect for a quick glance
- **Raw Mode**: File-by-file dependency details for developers who need everything

**Key Metrics**
- Total files and lines of code
- Per-file dependency counts
- Language distribution
- Largest files and most-dependent files
- File mapping with dependencies(for --dev/raw mode)     

**Zero External Dependencies**     
- Built entirely using the Python Standard Library.
- No external packages or `pip install` commands are required.


## Requirements
- Python 3.12+ (tested on Ubuntu 24.04 LTS)

> The code uses only Python standard libraries and should be compatible with Python 3.10+,
> but has been officially tested on Python 3.12.

## Build Instructions

```bash
git clone https://github.com/tecnolgd/repoScanner.git
```
```bash
cd repoScanner
```

### Tool Execution/Run

The easiest way to use repoScanner is with the provided shell script wrapper:

```bash
./reposcan <path> [--stats|--raw|--dev]
```

**Examples:**

- **Quick Summary** (Recommended)
```bash 
./reposcan .                      # Scan current directory (stats mode)
./reposcan /path/to/repo          # Scan a specific path (default: stats mode)
./reposcan /path/to/repo --stats  # Explicitly use stats mode
```

- **Detailed Analysis** (Developer Mode - Tree with File Mapping)
```bash
./reposcan /path/to/repo --raw    # File-by-file with dependency tree
./reposcan /path/to/repo --dev    # Same as --raw (alias)
```

The `--raw` / `--dev` mode displays all files in a tree structure with their dependencies mapped, perfect for detailed codebase analysis.

- **Get Help**
```bash
./reposcan --help                 # Show all available options
./reposcan -h    #Same as --help(alias)
```

#### Alternative: Direct Python Execution

- You can also run the scanner directly:

```bash
python3 -m repoScan.cli /path/to/repo          # Stats mode (default)
python3 -m repoScan.cli /path/to/repo --raw    # Detailed analysis with dependency tree
python3 -m repoScan.cli /path/to/repo --dev    # Same as --raw (alias)
```

- Help command
```bash
    python3 -m repoScan.cli /path/to/repo --help    # Same as -h
```

### Output
Reports are automatically saved to `output/report.json`

## Performance & Benchmarking

`repoScanner` includes a built-in automated performance profiling harness to track filesystem traversal latency and processing velocity across massive directory trees.

The benchmark suite programmatically allocates a temporary mock repository(`perf_test_sandbox`) containing thousands of deeply nested files across multiple language profiles (`.py`, `.cpp`, `.md`) to stress-test system I/O bounds, executes the scanner via the shell wrapper, and enforces strict post-run sandbox sanitation.

### Running the Benchmarks

To execute the performance suite and generate a local processing velocity report, run:

```bash
python3 tests/benchmark.py
```
or use shell command

```bash
./reposcan --bench
```

### Sample telemetry output

```txt
[✓] Pre-allocating mock codebase in 'tests/perf_test_sandbox' with 2500 files...

[✓] Launching tool environment execution via ./reposcan wrapper...

==================================================
           repoScanner Benchmark Suite            
==================================================
  Target Workspace        : tests/perf_test_sandbox
  Total Files Processed   : 2500
  Execution Time          : 0.38995 seconds
  I/O Processing Velocity : 6411.05 files/sec
==================================================
[✓] Flushed test sandbox environment directories cleanly.
```

## Supported Languages

Detects and maps **40+ extensions** to human-readable names, including:
* **Systems:** C, C++, Rust, Go, Zig, Swift
* **Web:** HTML, CSS, JavaScript, TypeScript, PHP
* **Data:** JSON, YAML, TOML, SQL, XML
* **Scripting:** Python, Ruby, Lua, Shell, PowerShell
* ...and many more. 
*(Unrecognized extensions fall back to their raw string format).*

## Documentation
* [Architecture](assets/docs/architecture.md)
* [Roadmap](assets/docs/roadmap.md)

## [Contributing](CONTRIBUTING.md)

## Contributors

A huge thanks to the developers contributing to repoScanner.
- [@Ghraven](https://github.com/Ghraven)
- [@AzarAI-TOP](https://github.com/AzarAI-TOP)


## Author & Version
- **Author:** tecnolgd
- **Version:** v0.2.0
- **License:** [MIT](LICENSE.md)