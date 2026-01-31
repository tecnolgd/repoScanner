#dependency.py
from ..utility.helpers import read_file_safely
from ..utility.helpers import extract_c_includes
from ..utility.helpers import extract_python_imports 

def dependency_analyzer(file_paths):
    all_dependencies = []
    
    # Handle single file (string) or list of files
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    
    for file_path in file_paths:
        lines = read_file_safely(file_path)
        
        if file_path.endswith(".py"):
            all_dependencies.extend(extract_python_imports(lines))
        elif file_path.endswith((".c", ".cpp", ".hpp", ".h")):
            all_dependencies.extend(extract_c_includes(lines))
    
    return all_dependencies
