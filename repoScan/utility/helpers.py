
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

def dependency_metrics(dep_report):
    total_lines = size(read_file_safely(file_path))

    include_based_files = size()
