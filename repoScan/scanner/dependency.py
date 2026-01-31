#dependency.py

def dependency_analyzer(file_path):
    dependencies={}

    for file in file_path:
        deps=extract_python_imports(file)
        if deps:
            dependencies[file] = deps

    return dependencies