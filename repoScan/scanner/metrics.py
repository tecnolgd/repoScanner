#metrics.py

from ..utility.helpers import (
    average_dependencies_per_file,
    average_file_size,
    average_lines_per_file,
    file_with_most_dependencies,
    get_max_file,
    get_total_bytes,
    language_metrics,
    largest_file_by_lines,
    total_bytes,
    total_dependencies,
    total_files,
    total_lines,
)


def generate_metrics(file_path, size_report, dep_report):
    return {
        "file_metrics": {
            "total": total_files(file_path),
            "total_bytes": total_bytes(size_report) if total_bytes(size_report) else get_total_bytes(file_path),
            "total_lines": total_lines(size_report),
            "average_lines": average_lines_per_file(size_report),
            "average_file_size": average_file_size(size_report),
            "largest_file": largest_file_by_lines(size_report),
            "max_file": get_max_file(size_report),
        },
        "dependency_metrics": {
            "total": total_dependencies(dep_report),
            "max_file": file_with_most_dependencies(dep_report),
            "average": average_dependencies_per_file(dep_report),
        },
        "language_metrics": language_metrics(file_path),
    }
