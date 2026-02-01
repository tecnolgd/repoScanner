#metrics.py

def generate_metrics(file_path, size_report, dep_report):
    return {
        "files": {
            "total": total_files(file_path),
            "total_lines": total_lines(size_report),
            "average_lines": average_lines_per_file(size_report),
            "largest_file": largest_file_by_lines(size_report),
        },
        "dependencies": {
            "total": total_dependencies(dep_report),
            "max_file": file_with_most_dependencies(dep_report),
            "average": average_dependencies_per_file(dep_report),
        },
        "languages": language_breakdown(file_path),
    }
