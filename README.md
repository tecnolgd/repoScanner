
<div align = "center">
<img src = "assets/repoScanner_logo.png" alt = "repoScanner logo">

<a href = "https://opensource.org/licenses/MIT"><img src = "https://img.shields.io/badge/License-MIT-green.svg" alt = "License: MIT"></a>
<a href = "https://www.python.org/downloads/"><img src = "https://img.shields.io/badge/Python-3.12%2B-blue" alt = "Python 3.7+"></a>
<img src = "https://img.shields.io/badge/interface-CLI-white">
<a href = "https://github.com/tecnolgd/repoScanner/releases"><img src = "https://img.shields.io/badge/Status-Beta-orange" alt = "Status: Beta"></a>
<a href = "#documentation"><img src = "https://img.shields.io/badge/docs-minimal-red" alt = "Docs: Minimal"></a>

</div>

>**repoScanner** is a lightweight repository analysis tool for developers.          
>Quickly understand your codebase structure, dependencies, and metrics with a single command.

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

## Requirements
- Python 3.12+ (tested on Ubuntu 24.04 LTS)

> The code uses only Python standard libraries and should be compatible with Python 3.10+,
> but has been officially tested on Python 3.12.

## Build Instructions

```bash
git clone https://github.com/tecnolgd/repoScanner.git
```
```bash
# 
cd repoScanner
```

### Tool Execution/Run

- **For Quick Summary** (Recommended)
```bash 
python3.12 -m repoScan.cli /path/to/repo #default mode(stats / nerd)
```
or
```bash
python3.12 -m repoScan.cli /path/to/repo --stats #or --nerd
```

- **For Detailed Analysis** (Developer Mode)
```bash
python3.12 -m repoScan.cli /path/to/repo --raw #or --dev
```

### Output
Reports are automatically saved to `output/report.json`

## Supported Languages

- **Python** (.py) - import detection
- **C/C++** (.c, .cpp, .h, .hpp) - #include detection

More languages coming in v0.1.1.

## Beta Status ⚠️

This is a **beta release**. Expect occasional improvements and refinements. Report issues and suggest features as you use it!

## Documentation
* [Architecture](assets/docs/architecture.md)
* [Roadmap](assets/docs/roadmap.md)

## [Contributing](CONTRIBUTING.md)


**Built for developers with the intent of saving time and peace-of-mind**

## Author & Version
- **Author:** tecnolgd
- **Version:** v0.1.0-beta
- **License:** [MIT](LICENSE.md)
