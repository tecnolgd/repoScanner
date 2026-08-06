<!--Architecture details and breakdown for repoScanner-->

## Architecture Overview

This document describes the high-level architecture of the repoScanner project, its key components, data flow, and guidance for extending or running the tool.

**Goals:**

- **Discoverable:** scan repository trees quickly and reliably.
- **Extensible:** add new analyzers and report formats with minimal changes.
- **Testable:** provide repeatable outputs suitable for benchmarking and CI.

**Core Components:**

- **scanner/**: Responsible for repository traversal and raw data collection (file lists, dependency hints, file sizes).     
Example files: [dirScanner.py](../../repoScan/scanner/dirScanner.py).
- **analyzer/**: Implements domain-specific analysis of the raw scan data. Current analyzers include size and structure analysis.      
Example files: [sizeAnalyzer.py](../../repoScan/analyzer/sizeAnalyzer.py), [structureAnalyzer.py](../../repoScan/analyzer/structureAnalyzer.py), [dependencyAnalyzer.py](../../repoScan/analyzer/dependencyAnalyzer.py).
- **scanner/metrics.py**: Aggregates basic metrics and performs derived calculations used by analyzers and reports.       
See [metrics.py](../../repoScan/scanner/metrics.py).
- **reports/**: Renders analysis results in multiple formats (`terminal`, `JSON`).        
Example files: [terminalReports.py](../../repoScan/reports/terminalReports.py), [jsonReports.py](../../repoScan/reports/jsonReports.py) and [htmlReports.py](../../repoScan/reports/htmlReports.py) (`htmlReports.py` is a placeholder at present).
- **vendor/libcvault**: Bundled native C++ library submodule that provides optional optimized file operations for the CLI.
- **reposcan**: Shell wrapper script that forwards scan commands to `python3 -m repoScan.cli` and also supports the benchmark harness via `--bench`.
- **cli.py**: CLI entrypoint and orchestration layer. Responsible for wiring together scanning, analysis, report generation, and optional `libcvault`-backed utility modes. See [cli.py](../../repoScan/cli.py).
- **output/**: Default location for produced artifacts such as `report.json`.
- **assets/data/**: Example and test data used by development and CI.     
Example: [testData.txt](../data/testData.txt).

**Data Flow**

1. The CLI triggers the scanner to walk the repository tree and collect raw file metadata.
2. The raw scan output is consumed by one or more **analyzers** (size, structure, dependency).
3. Analyzer outputs are aggregated by `metrics` to produce normalized statistics and summaries.
4. Results are handed to the reports layer to produce output artifacts (terminal summary, JSON files, or HTML pages placed under `output/`).

Mermaid overview:

```mermaid
flowchart TD
	
	Input[Input Path / Current Dir] --> CLI
	CLI --> Scanner

	subgraph Analyzers [The Analysis Core]
		Structure[Structure Analyzer]
		Size[Size Analyzer]
		Dependency[Dependency Analyzer]
	end

	Scanner --> Structure
	Scanner --> Size
	Scanner --> Dependency

	
	Structure --Report--> Raw_Analysis[Raw / Dev Analysis]
	Size --Size Report--> Raw_Analysis
	Dependency --Dependency Report--> Raw_Analysis

	Size --> Metrics[Generate Metrics]
	Dependency --> Metrics

	Metrics --> Stats[Stats / Nerd Analysis]
	Metrics --> JSON[JSON Report]
```

**Extension Points**

- Add a new analyzer: implement a new module under `repoScan/analyzer/` that accepts normalized scan data and returns structured results. Plug it into the CLI orchestration.
- Add a new report format: implement a new renderer under `repoScan/reports/` that consumes analyzer output and writes artifacts.
- Add new scanner rules: extend `repoScan/scanner/dirScanner.py` or add dependency heuristics in `repoScan/analyzer/dependencyAnalyzer.py` to include more file heuristics.

**Testing & Benchmarking**
- Unit tests and quick benchmarks live in `tests/` (for example, [tests/benchmark.py](../../tests/benchmark.py)). Use the sample data in `assets/data/` to create deterministic test cases.

## Sample execution

1. Run the CLI against a path to scan and display repo telemetry:

    ```bash
    python3 -m repoScan.cli . --stats //run from the repo 'repoScanner'
    ```

    Output:

    ```txt
     MODE: STATS/SUMMARY

    Repository Summary
    ==================

    File Metrics
    ------------
    Total files          : 308
    Total lines          : 5128
    Average lines/file   : 16
    Largest file         : ('./.git/objects/pack/pack-9196ac0a6218e2225604c3563ba93163ee061f7f.pack', 117398)

    Dependency Metrics
    ------------------
    Total dependencies   : 27
    File with most deps  : ./repoScan/cli.py
    Avg deps/file        : 0.09

    Language Breakdown
    ------------------
    Markdown             : 5
    TOML                 : 1
    .sample              : 14
    .0                   : 1
    .pack                : 1
    .rev                 : 1
    .idx                 : 1
    .png                 : 1
    .txt                 : 1
    Python               : 16
    JSON                 : 1
    .pyc                 : 10

    Generating JSON report...
    ✓ Report generated. Check: output/report.json
    ```


2. Run the benchmark script:

    ```bash
    python3 tests/benchmark.py 
    ```

    Output:

    ```txt
    [✓] Pre-allocating mock codebase in 'tests/perf_test_sandbox' with 2500 files...

    [✓] Launching tool environment execution via ./reposcan wrapper...

    ==================================================
             repoScanner Benchmark Suite
    ==================================================
      Target Workspace        : tests/perf_test_sandbox
      Total Files Processed   : 2500
      Execution Time          : 0.33595 seconds
      I/O Processing Velocity : 7441.56 files/sec
    ==================================================
    [✓] Flushed test sandbox environment directories cleanly.
    ```


**Design Notes & Rationale**

- Separation of concerns: scanning, analyzing, and reporting are intentionally decoupled to keep each component small and testable.
- Normalized intermediate model: analyzers consume a consistent data model produced by the scanner+metrics layer to simplify adding new analyzers.

**Next steps**

- Add sequence diagrams for complex analyzer interactions (optional).
- Expand the example JSON schema produced by `jsonReports` into a spec file for portability.
- HTML report generation via some module under `repoScan/reports`.
