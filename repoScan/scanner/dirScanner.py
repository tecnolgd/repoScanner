# Module for directory scanning - returns a list of files inside the directory with the complete path
import os

from .libcvault_wrapper import LIBCVAULT_AVAILABLE, populate_data, get_files

_cached_root = None
_cached_files = None


def dir_scanner(root_path):
    #Return list of file paths under root_path.
    #Uses `libcvault` if available, otherwise falls back to a pure-Python `os.walk` implementation so the tool works without native extensions

    global _cached_root, _cached_files
    root_path = os.path.abspath(root_path)

    if _cached_root == root_path and _cached_files is not None:
        return _cached_files

    if LIBCVAULT_AVAILABLE:
        populate_data(root_path)
        raw = get_files()
        if raw is None:
            _cached_root = root_path
            _cached_files = []
            return []
        files = [item if isinstance(item, str) else item[0] for item in raw]
    else:
        files = []
        for dirpath, _, filenames in os.walk(root_path):
            for fname in filenames:
                files.append(os.path.join(dirpath, fname))

    _cached_root = root_path
    _cached_files = files
    return files