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
    # For size_report from sizeAnalyzer, return average number of lines per file
    if isinstance(size_report, dict) and "average_lines" in size_report:
        return size_report.get("average_lines", 0)
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
    # dep_report is a list of dependencies
    if isinstance(dep_report, list):
        return len(dep_report)
    return sum(len(deps) for deps in dep_report.values()) if isinstance(dep_report, dict) else 0

def file_with_most_dependencies(dep_report):
    # dep_report is a list of dependencies
    if isinstance(dep_report, list):
        if not dep_report:
            return None
        # Return the most common dependency
        from collections import Counter
        return Counter(dep_report).most_common(1)[0][0]
    # Handle dict format if needed
    if not dep_report:
        return None
    return max(dep_report, key=lambda f: len(dep_report[f]))

def average_dependencies_per_file(dep_report):
    # dep_report is a list of dependencies
    if isinstance(dep_report, list):
        return len(dep_report) if dep_report else 0
    # Handle dict format if needed
    count = len(dep_report)
    if count == 0:
        return 0
    return total_dependencies(dep_report) / count

# Mapping of file extensions to human-readable language names.
# Fixes #3: extend coverage beyond Python and C/C++.
_EXTENSION_TO_LANGUAGE = {
    # Python
    ".py": "Python",
    ".pyw": "Python",
    ".pyi": "Python",
    # C / C++
    ".c": "C",
    ".h": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++",
    ".hxx": "C++",
    # JavaScript / TypeScript
    ".js": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    # Web
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "SCSS",
    # JVM
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".scala": "Scala",
    ".groovy": "Groovy",
    # .NET
    ".cs": "C#",
    ".vb": "Visual Basic",
    ".fs": "F#",
    # Systems
    ".rs": "Rust",
    ".go": "Go",
    ".swift": "Swift",
    ".zig": "Zig",
    # Scripting
    ".rb": "Ruby",
    ".php": "PHP",
    ".pl": "Perl",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".fish": "Shell",
    ".ps1": "PowerShell",
    ".lua": "Lua",
    ".r": "R",
    ".R": "R",
    # Data / Config
    ".sql": "SQL",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".xml": "XML",
    ".csv": "CSV",
    # Docs
    ".md": "Markdown",
    ".rst": "reStructuredText",
    ".tex": "LaTeX",
}


#language metrics function
def language_metrics(file_path):
    lang_counts = {}

    for file in file_path:
        ext = os.path.splitext(file)[1]
        if not ext:
            continue
        # Map extension to a readable language name when known,
        # otherwise fall back to the raw extension.
        language = _EXTENSION_TO_LANGUAGE.get(ext, ext)
        lang_counts[language] = lang_counts.get(language, 0) + 1

    return lang_counts

#'libcvault' based functions with pure python fallbacks

def sort_files_by_size(root_path):
    #Return a list of (size, path) tuples sorted by size descending.
    #Uses libcvault when available for performance, otherwise computes sizes via os.stat.

    if LIBCVAULT_AVAILABLE:
        #libcvault.populate_data(root_path)
        libcvault.sort_file_on_byte()
        results = []
        for i in range(libcvault.get_file_count()):
            name = libcvault.get_file_name(i)
            size = libcvault.get_file_size(i)
            results.append((size, name))
        return results

    files = dir_scanner(root_path)
    results = []
    for f in files:
        try:
            size = os.path.getsize(f)
        except Exception:
            size = 0
        results.append((size, f))
    results.sort(reverse=True)
    return results


def get_max_file(root_path):
    if LIBCVAULT_AVAILABLE:
        return libcvault.max_file()

    files = dir_scanner(root_path)
    max_file = None
    max_size = -1
    for f in files:
        try:
            s = os.path.getsize(f)
        except Exception:
            s = -1
        if s > max_size:
            max_size = s
            max_file = f
    return (max_file, max_size)


def search_file(root_path, filename):
    #Search for `filename` under `root_path` and return size or -3 if not found.

    if LIBCVAULT_AVAILABLE:
        #libcvault.populate_data(root_path)
        return libcvault.search_file(filename)

    files = dir_scanner(root_path)
    for f in files:
        if os.path.basename(f) == filename:
            try:
                return os.path.getsize(f)
            except Exception:
                return -1
    return -3


def line_count(file_path):
    try:
        with open(file_path, "r", errors="ignore") as fh:
            return sum(1 for _ in fh)
    except Exception:
        return -1


def get_total_bytes(root_path):
    if LIBCVAULT_AVAILABLE:
        libcvault.populate_data(root_path)
        return libcvault.get_total_bytes()

    total = 0
    for f in dir_scanner(root_path):
        try:
            total += os.path.getsize(f)
        except Exception:
            continue
    return total


#helper/guide function
def help_guide():
    helper_data = """repoScanner - Repository Analysis Tool

USAGE:
   python3 -m repoScan.cli <path> [--raw|--dev|--stats|--sort|--max|--search|--lc|--tbytes|--help]

ARGUMENTS:
    <path>          Directory path to scan (required)
    --stats         Show summary statistics (default)
    --raw, --dev    Show detailed file-by-file analysis with dependency tree
    --sort          Sort files by byte size using the bundled libcvault helper
    --max           Show the largest file using libcvault
    --search        Search for a file name using libcvault
    --lc            Show the line count for a file using libcvault
    --tbytes        Show total bytes across the scanned repository using libcvault
    --help, -h      Show this help message

EXAMPLES:
    # Scan current directory in stats mode
    python3 -m repoScan.cli .

    # Scan a specific path
    python3 -m repoScan.cli /path/to/repo          # Stats mode (default)


    # Show detailed analysis (tree with file dependencies)

    python3 -m repoScan.cli /path/to/repo --raw
    python3 -m repoScan.cli /path/to/repo --dev    # Same as --raw

    # Show advanced libcvault-backed utilities

    python3 -m repoScan.cli /path/to/repo --sort
    python3 -m repoScan.cli /path/to/repo --max
    python3 -m repoScan.cli /path/to/repo --search filename
    python3 -m repoScan.cli /path/to/repo --lc filename
    python3 -m repoScan.cli /path/to/repo --tbytes

    # Scan in explicit stats mode
    python3 -m repoScan.cli /path/to/repo --stats

    # Show tool usage
    python3 -m repoScan.cli /path/to/repo --help    # Same as -h

OUTPUT:
    Results are displayed in the terminal and saved to output/report.json
"""
    print(helper_data)