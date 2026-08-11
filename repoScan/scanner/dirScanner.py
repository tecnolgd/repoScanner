#module for directory scanning- returns a list of files inside the directory with the complete path
import os

def dir_scanner(root_path):
    scanned_files=[]

    for root,dir,files in os.walk(root_path):
        for f in files:
            full_path = os.path.join(root, f)
            scanned_files.append(full_path)
    
    return scanned_files

