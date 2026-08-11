
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
<h3 align = "center">repoScanner is a lightweight repository analysis tool for developers.</h3>          

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

**No Third-Party Python Packages Required**
- The core tool uses only the Python Standard Library for normal operation.
- An optional native helper (`vendor/libcvault`) provides optimized filesystem routines and requires a C++ toolchain and Python development headers to build.

## Benchmarks

> These numbers are obtained by testing the commands using [**hyperfine**](https://github.com/sharkdp/hyperfine).

### os.path vs std::recursive dir


| Mode | os.walk (ms) | std::recursive dir (ms) | Difference |
|---|---:|---:|---:|
| Shell wrapper --stats | 234.6 | 204.8 | std::directory is 29.8 ms faster |
| Shell wrapper --dev | 242.9 | 206.8 | std::directory is 36.1 ms faster |
| Direct Python --stats | 162.1 | 116.3 | std::directory is 45.8 ms faster |
| Direct Python --dev | 174.2 | 116.9 | std::directory is 57.3 ms faster |

### Modes using libcvault

| Operation | Command | Mean (ms) | Std Dev (ms) | Range (ms) | Runs |
|---|---|---:|---:|---|---:|
| search | `python3 -m repoScan.cli --search main.cpp` | 157.4 | 14.0 | 138.8–194.4 | 15 |
| total bytes | `python3 -m repoScan.cli --tbytes` | 166.0 | 19.2 | 144.7–219.9 | 13 |
| sort(size-based) | `python3 -m repoScan.cli --sort` | 162.2 | 14.0 | 140.4–193.3 | 15 |
| max file size| `python3 -m repoScan.cli --max` | 121.0 | 13.9 | 104.3–151.8 | 19 |
| file line count | `python3 -m repoScan.cli --lc README.md` | 124.5 | 15.2 | 106.5–153.6 | 20 |

> [!TIP]     
> For reproducing benchmarks, check [benchmarking using hyperfine](assets/docs/testing.md#reproducing-benchmarks).

## Requirements

- Python 3.12+ (tested on Ubuntu 24.04 LTS)

    > The code uses only Python standard libraries and should be compatible with Python 3.10+,
    > but has been officially tested on Python 3.12.


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
>   sudo apt-get install -y build-essential python3-dev
>   python3 -m pip install --user pybind11
>   ```
>
> - Compile using `pybind11` includes for portability:
>
>   ```bash
>   g++ -O3 -shared -std=c++17 -fPIC   -I 
>   usr/local/lib/python3.12/dist-packages/
>   pybind11/include   -I/usr/include/
>   python3.12   -I vendor/libcvault   
>   vendor/bridge.cpp vendor/libcvault/
>   main.cpp   -o libcvault$
>   (python3-config --extension-suffix)
>    ```


> [!IMPORTANT]
> 1. The `vendor/libcvault` native helper uses Python's C/C++ bindings (pybind11 bridge) for optimized file system operations.
> 2. Building the helper requires a C++ compiler (e.g., `g++`) and Python development headers. 
> 3. The native helper is optional. If you prefer zero native dependencies, you can safely add `.gitmodules` and `vendor/` to your `.gitignore`.

The repository may include a prebuilt binary (e.g. `libcvault.cpython-312-x86_64-linux-gnu.so`) for convenience; if you plan to distribute, prefer providing prebuilt wheels rather than committing `.so` artifacts in the repo.

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
