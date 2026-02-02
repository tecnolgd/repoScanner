#metrics.py

from ..utility.helpers import file_with_most_dependencies
from ..utility.helpers import total_files
from ..utility.helpers import total_lines
from ..utility.helpers import language_metrics
from ..utility.helpers import average_lines_per_file
from ..utility.helpers import average_lines_per_file
from ..utility.helpers import average_dependencies_per_file
from ..utility.helpers import largest_file_by_lines
from ..utility.helpers import total_dependencies

def generate_metrics(file_path, size_report, dep_report):
    return {
        "file_metrics": {
            "total": total_files(file_path),
            "total_lines": total_lines(size_report),
            "average_lines": average_lines_per_file(size_report),
            "largest_file": largest_file_by_lines(size_report),
        },
        "dependency_metrics": {
            "total": total_dependencies(dep_report),
            "max_file": file_with_most_dependencies(dep_report),
            "average": average_dependencies_per_file(dep_report),
        },
        "language_metrics": language_metrics(file_path),
    }
