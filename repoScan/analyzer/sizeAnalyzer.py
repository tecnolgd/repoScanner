#sizeAnalyzer.py

import os
from collections import defaultdict

def size_analyzer(file_path):
    size_data={
        "total_files": 0,
        "total_bytes": 0,
        "average_file_size": 0,
        "largest_files": [],
        "size_by_extension": defaultdict(int)
    }

    file_sizes = []

    for path in file_path:
        try:
            size=os.path.getsize(path)
        except OsError:
            continue

        size_data["total_files"] +=1
        size_data["total_bytes"] +=size
        file_sizes.append((path, size))

        _, extension = os.path.splitext(path)
        if extension:
            size_data["size_by_extension"][extension] += size

    if size_data["total_files"] >0:
        size_data["average_file_size"]=(size_data["total_bytes"]//size_data["total_files"])

    file_sizes.sort(key=lambda x: x[1], reverse=True)
    size_data["largest_files"] = file_sizes[:5]

    size_data["size_by_extension"] = dict(size_data["size_by_extension"])

    return size_data