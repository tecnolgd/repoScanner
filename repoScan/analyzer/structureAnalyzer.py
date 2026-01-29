#structureAnalyzer.py
import os
from collections import defaultdict

def structure_analyzer(file_path):
    repo_structure={
        "total_files": 0,
        "directories": set(),
        "file_extentions": defaultdict(int),
        "files/directory": defaultdict(int),
        "max_depth": 0
    }

    for path in file_path:
        repo_structure["total_files"]+=1
        directory=os.path.dirname(path)
        repo_structure["directories"].add(directory)
        repo_structure["files/directory"][directory]+=1
        _, extention=os.path.splitext(path)
        if extention:
            repo_structure["file_extentions"][extention]+=1

        depth= path.count(os.sep)
        repo_structure["max_depth"]=max(repo_structure["max_depth"], depth)
    
    repo_structure["total_directories"]=len(repo_structure["directories"])
    repo_structure["directories"]= list(repo_structure["directories"])

    return repo_structure
