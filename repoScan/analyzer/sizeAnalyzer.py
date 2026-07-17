# sizeAnalyzer.py - Analyze file sizes and line counts

import os
from collections import defaultdict
from ..utility.helpers import read_file_safely


def size_analyzer(file_paths):
    """
    Analyze file sizes and line counts for a list of file paths.
    
    Returns a dict with:
    - file_sizes: dict of file_path -> size in bytes
    - total_size_bytes: total size of all files
    - average_file_size: average file size in bytes
    - largest_files: top 10 files by size [(path, size), ...]
    - file_line_counts: dict of file_path -> line count
    - total_lines: total lines across all files
    - average_lines_per_file: average lines per file
    - largest_files_by_lines: top 10 files by line count [(path, lines), ...]
    """
    file_sizes = {}
    total_size = 0
    largest_files = []
    file_line_counts = {}
    total_lines = 0
    largest_files_by_lines = []

    # Handle single file (string) or list of files
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    for file_path in file_paths:
        try:
            size = os.path.getsize(file_path)
            file_sizes[file_path] = size
            total_size += size
            largest_files.append((file_path, size))
        except OSError:
            # skip files that can't be read
            continue

        # Count lines
        try:
            lines = read_file_safely(file_path)
            line_count = len(lines)
            file_line_counts[file_path] = line_count
            total_lines += line_count
            largest_files_by_lines.append((file_path, line_count))
        except Exception:
            # skip files that can't be read for line counting
            continue

    # sort by size descending and take top 10
    largest_files.sort(key=lambda x: x[1], reverse=True)
    top_10_by_size = largest_files[:10]

    # sort by line count descending and take top 10
    largest_files_by_lines.sort(key=lambda x: x[1], reverse=True)
    top_10_by_lines = largest_files_by_lines[:10]

    return {
        "file_sizes": file_sizes,
        "total_size_bytes": total_size,
        "average_file_size": total_size // len(file_sizes) if file_sizes else 0,
        "largest_files": top_10_by_size,
        "file_line_counts": file_line_counts,
        "total_lines": total_lines,
        "average_lines_per_file": total_lines // len(file_line_counts) if file_line_counts else 0,
        "largest_files_by_lines": top_10_by_lines
    }