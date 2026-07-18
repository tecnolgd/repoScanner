#sizeAnalyzer.py

import os
from collections import defaultdict

def size_analyzer(file_path):
    size_data={
        "total_files": 0,
        "total_bytes": 0,
        "average_file_size": 0,
        "total_lines": 0,
        "average_lines": 0,
        "largest_files": [],
        "size_by_extension": defaultdict(int)
    }

    file_sizes = []

    for path in file_path:
        try:
            size=os.path.getsize(path)
        except OSError:
            continue

        size_data["total_files"] +=1
        size_data["total_bytes"] +=size
        file_sizes.append((path, size))

        # Count lines where possible
        try:
            with open(path, "r", errors="ignore") as fh:
                lines = sum(1 for _ in fh)
        except Exception:
            lines = 0
        size_data["total_lines"] += lines

        _, extension = os.path.splitext(path)
        if extension:
            size_data["size_by_extension"][extension] += size

    if size_data["total_files"] >0:
        size_data["average_file_size"]=(size_data["total_bytes"]//size_data["total_files"])
        size_data["average_lines"] = (size_data["total_lines"]//size_data["total_files"]) if size_data["total_lines"]>0 else 0

    file_sizes.sort(key=lambda x: x[1], reverse=True)
    size_data["largest_files"] = file_sizes[:5]
    size_data["size_by_extension"] = dict(size_data["size_by_extension"])

    return size_data