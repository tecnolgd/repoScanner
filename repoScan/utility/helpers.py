import os

def read_file_safely(file_path):
    try:
        with open(file_path, "r", errors="ignore") as f:
            return f.readlines()
    except Exception:
        return []


#check for python imports
def extract_python_imports(lines):
    imports = set()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("import "):
            parts = line.replace("import", "").split(",")
            for p in parts:
                imports.add(p.strip().split()[0])

        elif line.startswith("from "):
            parts = line.split()
            if len(parts) >= 2:
                imports.add(parts[1])

    return list(imports)

#check for C/C++ includes
def extract_c_includes(lines):
    includes = set()

    for line in lines:
        line = line.strip()
        if line.startswith("#include"):
            start = line.find("<")
            end = line.find(">")
            if start != -1 and end != -1:
                includes.add(line[start+1:end])

    return list(includes)

#helper functions for metrics generation

#file metrics functions
def total_files(file_path):
    return len(file_path)

def total_lines(size_report):
    # size_report is already a dict with totals from sizeAnalyzer
    if isinstance(size_report, dict) and "total_lines" in size_report:
        return size_report.get("total_lines", 0)
    return 0

def average_lines_per_file(size_report):
    # For size_report from sizeAnalyzer, use average_file_size
    if isinstance(size_report, dict) and "average_file_size" in size_report:
        return size_report.get("average_file_size", 0)
    return 0

def largest_file_by_lines(size_report):
    # For size_report from sizeAnalyzer, return largest files
    if isinstance(size_report, dict) and "largest_files" in size_report:
        files = size_report.get("largest_files", [])
        if files:
            return files[0]  # Returns (path, size) tuple
    return None

#dependency metrics functions
def total_dependencies(dep_report):
    return sum(len(deps) for deps in dep_report.values())

def file_with_most_dependencies(dep_report):
    if not dep_report:
        return None
    return max(dep_report, key=lambda f: len(dep_report[f]))

def average_dependencies_per_file(dep_report):
    count = len(dep_report)
    if count == 0:
        return 0
    return total_dependencies(dep_report) / count

#language metrics function
def language_metrics(file_path):
    language_metrics = {}

    for file in file_path:
        ext = os.path.splitext(file)[1]
        if not ext:
            continue
        language_metrics[ext] = language_metrics.get(ext, 0) + 1

    return language_metrics



