
<div align = "center">

<img src = "assets/repoScanner_logo.png" alt = "repoScanner logo">

<a href = "LICENSE.md">
<img src = "https://img.shields.io/badge/license-MIT-1a1a1a?style=flat-square" alt = "License: MIT"></a>
<a href = "https://www.python.org/downloads/">
<img src = "https://img.shields.io/badge/python-3.12+-1a1a1a?style=flat-square&logo=python&logoColor=888888" alt = "Python: 3.12+"></a>
<a href = "https://github.com/tecnolgd/repoScanner">
<img src = "https://img.shields.io/badge/interface-CLI-1a1a1a?style=flat-square" alt = "Interface: CLI"></a>
<a href = "https://github.com/tecnolgd/repoScanner/releases">
<img src="https://img.shields.io/github/v/release/tecnolgd/blog-tecnolgd?color=1a1a1a&style=flat-square" alt="Version"></a>
<a href = "#documentation">
<img src = "https://img.shields.io/badge/docs-available-1a1a1a?style=flat-square" alt = "Docs: Available"></a>
<a href = "https://github.com/tecnolgd/libcvault"><img src = "https://img.shields.io/badge/submodule-libcvault-1a1a1a?style=flat-square" alt = "Submodule: libcvault"></a>

</div>

---

**repoScanner** is a lightweight repository analysis tool for developers.          

- Quickly understand your codebase structure, dependencies, and metrics with a single command.
- Built for developers with the intent of saving time and peace-of-mind

## What It Does

- **Directory Analysis**: Scan total files, lines of code, average file size, etc.
- **Dependency Detection**: Extract and map dependencies (Python imports, C/C++ includes)
- **Language Breakdown**: See what languages dominate your repo
- **Smart Reporting**: Choose between quick stats or detailed developer mode
- **JSON Export**: Machine-readable reports for automation
- **Native File Utilities**: Optional `vendor/libcvault` submodule supports advanced CLI file sorting, search, and byte/line metrics when initialized.

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

## Benchmarks

These numbers are obtained by testing the commands using hyperfine.

| Scenario | Command | Mean (ms) | Std Dev (ms) | Range (ms) | Runs |
|---|---|---:|---:|---|---:|
| OS walk, shell wrapper | `./reposcan --stats` | 234.6 | 19.0 | 215.6–284.4 | 10 |
| std::directory, shell wrapper | `./reposcan --stats` | 204.8 | 15.5 | 185.6–238.3 | 12 |
| Direct Python mode | `python3 -m repoScan.cli --stats` | 116.3 | 9.5 | 105.6–145.0 | 20 |
| Direct Python mode | `python3 -m repoScan.cli --dev` | 116.9 | 8.4 | 109.2–138.0 | 21 |
| libcvult mode | `python3 -m repoScan.cli --search main.cpp` | 157.4 | 14.0 | 138.8–194.4 | 15 |
| libcvult mode | `python3 -m repoScan.cli --tbytes` | 166.0 | 19.2 | 144.7–219.9 | 13 |
| libcvult mode | `python3 -m repoScan.cli --sort` | 162.2 | 14.0 | 140.4–193.3 | 15 |
| libcvult mode | `python3 -m repoScan.cli --help` | 116.8 | 12.4 | 102.0–146.5 | 20 |
| libcvult mode | `python3 -m repoScan.cli --max` | 121.0 | 13.9 | 104.3–151.8 | 19 |
| libcvult mode | `python3 -m repoScan.cli --lc README.md` | 124.5 | 15.2 | 106.5–153.6 | 20 |

> [!TIP]     
> For reproducing benchmarks and additional details, check [benchmarking using hyperfine]().

## Requirements

- Python 3.12+ (tested on Ubuntu 24.04 LTS)

> The code uses only Python standard libraries and should be compatible with Python 3.10+,
> but has been officially tested on Python 3.12.

## Build Instructions

### 1. Setup

```bash
git clone https://github.com/tecnolgd/repoScanner.git
```
```bash
cd repoScanner
```

<details>
<summary><b>Optional <code>libcvault</code> native helper</b> (advanced CLI modes)</summary>
<br>


> **NOTE**:       
> Core `repoScanner` functionality is pure Python (zero external dependencies). The `vendor/libcvault` native helper uses Python's C/C++ bindings (pybind11 bridge) for optimized file system operations.


The core `repoScanner` functionality is pure Python and does not require external packages beyond a Python interpreter.
The `vendor/libcvault` submodule provides optional native helpers used only for advanced CLI modes such as `--sort`, `--max`, `--search`, `--lc`, and `--tbytes`.

- To fetch the bundled native helper after cloning the repository:

    ```bash
    git submodule update --init --recursive vendor/libcvault
    ```

    - `git submodule init` registers the submodule in your local repo configuration.
    - `git submodule update --init` also clones and checks out the correct commit for the submodule.

- If you later want to refresh `libcvault` from its remote repository, run:

    ```bash
    git submodule update --remote vendor/libcvault
    ```

    This updates the submodule to the latest commit from its configured branch. You should then review and commit the updated submodule pointer in the main repo.

- If you want to use the advanced `libcvault`-backed CLI modes, build the native extension from `bridge.cpp` and `vendor/libcvault/main.cpp`.

    ```bash
    g++ -O3 -shared -std=c++17 -fPIC   -I/usr/local/lib/python3.12/dist-packages/pybind11/include   -I/usr/include/python3.12   -I vendor/libcvault   vendor/bridge.cpp vendor/libcvault/main.cpp   -o libcvault$(python3-config --extension-suffix)
    ```

</details>


### 2. Tool Execution/Run

The easiest way to use repoScanner is with the provided shell script wrapper:

```bash
./reposcan <path> [--stats|--raw|--dev|--bench]
```

**Quick start:**

```bash
./reposcan .                       # stats mode
./reposcan /path/to/repo --raw     # detailed developer output
./reposcan /path/to/repo --bench   # benchmark harness
```

### 3. Output
Reports are automatically saved to `output/report.json`

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


## Author & License
- **Author:** tecnolgd
- **License:** [MIT](LICENSE.md)
