#cli.py --> command line interface for automation tool
#cd /home/chief/projects/repoScanner && python3 -m repoScan.cli 2>&1 (exection command)

import sys

from .analyzer.dependencyAnalyzer import dependency_analyzer
from .scanner.dirScanner import dir_scanner
from .utility.helpers import (
    sort_files_by_size,
    get_max_file,
    search_file,
    line_count,
    get_total_bytes,
)
from .analyzer.structureAnalyzer import structure_analyzer
from .analyzer.sizeAnalyzer import size_analyzer
from .scanner.metrics import generate_metrics
from .reports.terminalReports import print_summary, print_raw_analysis
from .reports.jsonReports import write_json_report
from .utility.helpers import help_guide

# Task to be completed

# - Plan about handling dir scans via libcvault only if possible
# - Upgrades to algorithms for higher perf.
# - Update the same in 'reposcan' bash script as well as update the required docs and help sections as well
# - The next stage would be using reposcanner in piped instructions using streams

# Dev notes
# - To create the .so:
    # g++ -O3 -shared -std=c++17 -fPIC   -I/usr/local/lib/python3.12/dist-packages/pybind11/include   -I/usr/include/python3.12   -I vendor/libcvault   vendor/bridge.cpp vendor/libcvault/main.cpp   -o libcvault$(python3-config --extension-suffix)
# - To update the library in 'repoScanner'
    # git submodule update --remote libcvault


def main():
    # Parse arguments
    root = "."
    mode = "stats"  # Default mode
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ["--raw", "--dev"]:
            mode = "raw"
        elif arg in ["--stats", "--nerd"]:
            mode = "stats"
        elif arg in ["--help", "-h"]:
            mode = "help"
        elif arg in ["--max"]:
            mode = "max"
        elif arg in ["--tbytes"]:
            mode = "tbytes"
        elif arg in ["--sort"]:
            mode = "sort"
        elif arg in ["--search", "--lc"]:
            mode = arg.lstrip("-") #removes '-' from the arg dynamically avoiding confusions in choosing the mode from the list

            if i + 1 < len(args):
                file_name = args[i + 1]
                i += 1  # Advance past the filename value
            else:
                print(f"Error: {arg} requires a filename argument.")
                sys.exit(1)
        else:
            root = arg
        i += 1    

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
    elif mode == "sort":

        print("\nSorted Directory (by byte size):")
        results = sort_files_by_size(root)
        for size, name in results:
            print(f"{size:>10} bytes  |  {name}")
    elif mode == "max":
        max_info = get_max_file(root)
        if isinstance(max_info, tuple):
            print('Largest file: ', max_info)
        else:
            print('Largest file: ', max_info)

    elif mode == "search":
        result = search_file(root, file_name)
        if result != -3:
            print(f"File found: {file_name}[{result} bytes]")
        else:
            print("File NOT found")

    elif mode == "lc":
        print(f"Line count of {file_name}: {line_count(file_name)}")
    elif mode == "tbytes":
        print('Total bytes:', get_total_bytes(root))
    else:
        print("Invalid Mode!")


    # Always generate JSON report
    print("\nGenerating JSON report...")
    json_path = write_json_report(metrics)
    print(f"✓ Report generated. Check: {json_path}")


if __name__ == "__main__":
    main()
