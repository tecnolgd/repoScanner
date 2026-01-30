#module for directory scanning- returns a list of files inside the directory with the complete path
import os
from ..analyzer.structureAnalyzer import structure_analyzer
def dir_scanner(root_path):
    scanned_files=[]

    for root,dir,files in os.walk(root_path):
        for f in files:
            full_path = os.path.join(root, f)
            scanned_files.append(full_path)
    
    return scanned_files
count=0
print("file data:")
for f in dir_scanner("/home/chief/projects/repoScanner/repoScan"): #absolute path of the directory
    count+=1
    print(count,"-->",f)
    
files= dir_scanner("/home/chief/projects/repoScanner/repoScan")
report = structure_analyzer(files)
print("Repo structure analysis:")
print(report)
#cd /home/chief/projects/repoScanner && python3 -m repoScan.scanner.dirScanner 2>&1