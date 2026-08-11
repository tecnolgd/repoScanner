# Module for directory scanning - returns a list of files inside the directory with the complete path
import os

try:
    import libcvault  # optional native helper (pybind11 extension)
    LIBCVAULT_AVAILABLE = True
except Exception:
    libcvault = None
    LIBCVAULT_AVAILABLE = False


def dir_scanner(root_path):
    """Return list of file paths under root_path.

    Uses `libcvault` if available for speed; otherwise falls back to a pure-Python
    `os.walk` implementation so the tool works without native extensions.
    """
    if LIBCVAULT_AVAILABLE:
        libcvault.populate_data(root_path)
        raw = libcvault.get_files()
        if raw is None:
            return []
        return [item[0] for item in raw]

    # Pure-Python fallback
    scanned_files = []
    for dirpath, _, files in os.walk(root_path):
        for fname in files:
            scanned_files.append(os.path.join(dirpath, fname))
    return scanned_files


def sort_files_by_size(root_path):
    """Return a list of (size, path) tuples sorted by size descending.

    Uses libcvault when available for performance, otherwise computes sizes
    via os.stat.
    """
    if LIBCVAULT_AVAILABLE:
        libcvault.populate_data(root_path)
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
    """Search for `filename` under `root_path` and return size or -3 if not found."""
    if LIBCVAULT_AVAILABLE:
        libcvault.populate_data(root_path)
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

