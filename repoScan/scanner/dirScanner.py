#module for directory scanning- returns a list of files inside the directory with the complete path
import os
import libcvault

def dir_scanner(root_path):
    scanned_files = []
    libcvault.populate_data(root_path)
    # libcvault.get_files() returns a list of (name, size) tuples; extract names
    raw = libcvault.get_files()
    if raw is None:
        return []

    scanned_files = [item[0] for item in raw]

    return scanned_files

