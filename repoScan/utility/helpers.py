
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
    return sum(info.get("lines", 0) for info in sizes.values())

def average_lines_per_file(size_report):
    count = len(sizes)
    if count == 0:
        return 0
    return total_lines(sizes) / count

def largest_file_by_lines(sizes):
    if not sizes:
        return None
    return max(sizes, key=lambda f: sizes[f].get("lines", 0))

#dependency metrics functions
def total_dependencies(dep_report):
    return sum(len(deps) for deps in dep_report.values())

def file_with_most_dependencies(dep_report):
    if not dependencies:
        return None
    return max(dep_report, key=lambda f: len(dep_report[f]))
