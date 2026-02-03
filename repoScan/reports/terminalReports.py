#terminalReports.py

# Section printer
def print_section(title):
    print("\n" + title)
    print("-" *len(title))

# Key-value printer
def print_kv(label, value, width=20):
    print(f"{label.ljust(width)} : {value}")


def print_file_metrics(file_metrics):
    print_section("File Metrics")
    print_kv("Total files", file_metrics["total"])
    print_kv("Total lines", file_metrics["total_lines"])
    print_kv("Average lines/file", round(file_metrics["average_lines"], 2))
    print_kv("Largest file", file_metrics["largest_file"])

def print_dependency_metrics(dependency_metrics):
    print_section("Dependency Metrics")
    print_kv("Total dependencies", dependency_metrics["total"])
    print_kv("File with most deps", dependency_metrics["max_file"])
    print_kv("Avg deps/file", round(dependency_metrics["average"], 2))

def print_language_metrics(language_metrics):
    print_section("Language Breakdown")
    for lang, count in language_metrics.items():
        print_kv(lang, count)

# Summmary printer
def print_summary(metrics):
    print("\nRepository Summary")
    print("=" * 18)

    print_file_metrics(metrics["file_metrics"])
    print_dependency_metrics(metrics["dependency_metrics"])
    print_language_metrics(metrics["language_metrics"])


# Raw/Developer mode - shows detailed file and dependency data
def print_raw_dependencies(dep_report):
    fcount = 0
    print_section("Dependencies (Raw Details)")
    for file_path, dependencies in dep_report.items():
        fcount+=1
        print(f"\n{fcount} --> {file_path}")
        if dependencies:
            for dep in dependencies:
                print(f"   ├─ {dep}")
            print(f"   └─ [{len(dependencies)} dependencies]")
        else:
            print("   └─ [No dependencies]")


def print_raw_analysis(files, structure_report, size_report, dep_report):
    print_section("Complete Analysis (Raw Mode)")
    print_kv("Total files scanned", len(files))
    print("\n")
    print_raw_dependencies(dep_report)

