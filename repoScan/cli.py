#cli.py --> command line interface for automation tool
#cd /home/chief/projects/repoScanner && python3 -m repoScan.cli 2>&1 (exection command)
from .scanner.dependency import dependency_analyzer
from .scanner.dirScanner import dir_scanner
from .analyzer.structureAnalyzer import structure_analyzer
from .analyzer.sizeAnalyzer import size_analyzer
from .scanner.metrics import generate_metrics
from .reports.terminalReports import print_summary

count=0
print("file data:")
for f in dir_scanner("/home/chief/projects/repoScanner/repoScan"): #absolute path of the directory
    count+=1
    print(count,"-->",f)

files= dir_scanner("/home/chief/projects/repoScanner/repoScan")
report = structure_analyzer(files)
print(" ")

print("Repo structure analysis:")
print(report)
print(" ")

print("Repo size anaysis:")
size_report=size_analyzer(files)
print(size_report)
print(" ")

print("Dependency analysis:")
dep_report=dependency_analyzer(files)
print(dep_report)
print(" ")

metrics = generate_metrics(files, size_report, dep_report)
print("Metrics for nerds:")
print_summary(metrics)

#cd /home/chief/projects/repoScanner && python3 -m repoScan.cli 2>&1 (cmd to run the script) or 
# python3 -m repoScan.cli
