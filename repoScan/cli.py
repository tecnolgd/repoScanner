#cli.py --> command line interface for automation tool
#cd /home/chief/projects/repoScanner && python3 -m repoScan.cli 2>&1 (exection command)

import sys
import libcvault #external library(git submodule)

from .analyzer.dependencyAnalyzer import dependency_analyzer
from .scanner.dirScanner import dir_scanner
from .analyzer.structureAnalyzer import structure_analyzer
from .analyzer.sizeAnalyzer import size_analyzer
from .scanner.metrics import generate_metrics
from .reports.terminalReports import print_summary, print_raw_analysis
from .reports.jsonReports import write_json_report
from .utility.helpers import help_guide

# Task to be completed

# - Add all the required function calls for various features and flags
# - Update the same in 'reposcan' bash script as well as update the required docs and help sections as well
# - The next stage would be using reposcanner in piped instructions using streams

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
        libcvault.populate_data(root)
        libcvault.sort_file_on_byte() # Sorts vector in place
    
        # Iterate through C++ memory cleanly via getters
        for i in range(libcvault.get_file_count()):
            name = libcvault.get_file_name(i)
            size = libcvault.get_file_size(i)
            print(f"{size:>10} bytes  |  {name}") 

    elif mode == "max":
        print('Largest file: ', libcvault.max_file())
    elif mode == "search":
        libcvault.populate_data(root)
        result = libcvault.search_file(file_name)
        if result != -3:
            print(f"File found: {file_name}[{result} bytes]")
        else:
            print("File NOT found")
    elif mode == "lc":
        print(f"Line count of {file_name}: {libcvault.line_count(file_name)}")
    elif mode == "tbytes":
        libcvault.populate_data(root); 
        print('Total bytes:', libcvault.get_total_bytes())
    else:
        print("Invalid Mode!")


    # Always generate JSON report
    print("\nGenerating JSON report...")
    json_path = write_json_report(metrics)
    print(f"✓ Report generated. Check: {json_path}")


if __name__ == "__main__":
    main()
