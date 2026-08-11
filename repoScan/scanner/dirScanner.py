# Module for directory scanning - returns a list of files inside the directory with the complete path
import os

try:
    import libcvault  # optional native helper (pybind11 extension)
    LIBCVAULT_AVAILABLE = True
except Exception:
    libcvault = None
    LIBCVAULT_AVAILABLE = False


def dir_scanner(root_path):
    #Return list of file paths under root_path.
    #Uses `libcvault` if available, otherwise falls back to a pure-Python `os.walk` implementation so the tool works without native extensions

    if LIBCVAULT_AVAILABLE:
        libcvault.populate_data(root_path)
        raw = libcvault.get_files()
        if raw is None:
            return []
        # libcvault.get_files() returns a list of file path strings.
        # If it returns tuples, preserve compatibility by extracting the first element.
        return [item if isinstance(item, str) else item[0] for item in raw]

    # Pure-Python fallback
    scanned_files = []
    for dirpath, _, files in os.walk(root_path):
        for fname in files:
            scanned_files.append(os.path.join(dirpath, fname))
    return scanned_files