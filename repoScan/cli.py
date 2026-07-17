#cli.py --> command line interface for automation tool
#cd /home/chief/projects/repoScanner && python3 -m repoScan.cli 2>&1 (exection command)

import sys
from .analyzer.dependencyAnalyzer import dependency_analyzer
from .scanner.dirScanner import dir_scanner
from .analyzer.structureAnalyzer import structure_analyzer
from .analyzer.sizeAnalyzer import size_analyzer
from .scanner.metrics import generate_metrics
from .reports.terminalReports import print_summary, print_raw_analysis
from .reports.jsonReports import write_json_report
from .utility.helpers import help_guide

def main():
    # Parse arguments
    root = "."
    mode = "stats"  # Default mode
    
    for arg in sys.argv[1:]:
        if arg in ["--raw", "--dev",]:
            mode = "raw"
        elif arg in ["--stats", "--nerd"]:
            mode = "stats"
        elif arg in ["--help", "-h"]:
            mode = "help"
        else:
            root = arg
    
    files = dir_scanner(root)
    report = structure_analyzer(files)
    size_report = size_analyzer(files)
    dep_report = dependency_analyzer(files)
    metrics = generate_metrics(files, size_report, dep_report)
    
    # Output based on mode
    if mode == "raw":
        print("\nMODE: RAW/DEVELOPER")
        print_raw_analysis(files, report, size_report, dep_report)
    elif mode == "stats":  # stats mode (default)
        print("\n MODE: STATS/SUMMARY")
        print_summary(metrics)
    elif mode == "help":
        help_guide()
        sys.exit(0)
    else:
        print("Invalid Mode!")


    # Always generate JSON report
    print("\nGenerating JSON report...")
    json_path = write_json_report(metrics)
    print(f"✓ Report generated. Check: {json_path}")


if __name__ == "__main__":
    main()
