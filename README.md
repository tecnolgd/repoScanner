# repoScanner

**A lightweight repository analysis tool for developers.**

Quickly understand your codebase structure, dependencies, and metrics with a single command.

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

## Usage

### Quick Summary (Recommended)
```bash
python3 -m repoScan.cli /path/to/repo
```
or
```bash
python3 -m repoScan.cli /path/to/repo --stats #or nerd
```

### Detailed Analysis (Developer Mode)
```bash
python3 -m repoScan.cli /path/to/repo --raw #or --dev
```

### Output
Reports are automatically saved to `output/report.json`

## Supported Languages

- **Python** (.py) - import detection
- **C/C++** (.c, .cpp, .h, .hpp) - #include detection

More languages coming in v0.1.1.


## Beta Status ⚠️

This is a **beta release**. Expect occasional improvements and refinements. Report issues and suggest features as you use it!

## Coming Soon

- HTML report generation
- More language support (JavaScript, Go, Rust)
- Gitignore integration
- Circular dependency detection

---

**Built for developers with the intent of saving time and peace-of-mind**
