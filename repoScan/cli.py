#cli.py --> command line interface for automation tool
#cd /home/chief/projects/repoScanner && python3 -m repoScan.cli 2>&1 (exection command)

from .scanner.dirScanner import dir_scanner
from .analyzer.structureAnalyzer import structure_analyzer
from .analyzer.sizeAnalyzer import size_analyzer


count=0
print("file data:")
for f in dir_scanner("/home/chief/projects/repoScanner/repoScan"): #absolute path of the directory
    count+=1
    print(count,"-->",f)

files= dir_scanner("/home/chief/projects/repoScanner/repoScan")
report = structure_analyzer(files)
print("Repo structure analysis:")
print(report)

print("Repo size anaysis:")
size_report=size_analyzer(files)
print(size_report)