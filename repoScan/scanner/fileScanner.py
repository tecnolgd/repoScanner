#module for directory scanning- returns a list of files inside the directory with the complete path
import os

def dirScanner(root_path):
    scanned_files=[]

    for root,dir,files in os.walk(root_path):
        for f in files:
            full_path = os.path.join(root, f)
            scanned_files.append(full_path)
    
    return scanned_files

print("file data:")
for f in dirScanner("/home/chief/projects/repoScanner/repoScan"): #absolute path of the directory
    print(f)