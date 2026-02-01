#metrics.py

def metrics(file_path, size_report, dep_report){
    "file_metrics": file_metrics(file_path, size_report),
    "dependency_metrics": dependency_metrics(dep_report),
    "language_metrics": language_metrics(file_path)
}