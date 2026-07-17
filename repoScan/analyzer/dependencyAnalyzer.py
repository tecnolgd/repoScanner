from ..utility.helpers import read_file_safely
from ..utility.helpers import extract_c_includes
from ..utility.helpers import extract_python_imports


def dependency_analyzer(file_paths):
    file_dependencies = {}

    # Handle single file (string) or list of files
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    for file_path in file_paths:
        lines = read_file_safely(file_path)
        dependencies = []

        if file_path.endswith(".py"):
            dependencies.extend(extract_python_imports(lines))
        elif file_path.endswith((".c", ".cpp", ".hpp", ".h")):
            dependencies.extend(extract_c_includes(lines))

        file_dependencies[file_path] = dependencies

    return file_dependencies
