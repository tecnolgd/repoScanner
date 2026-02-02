#terminalReports.py

#section printer
def print_section(title):
    print("\n" + title)
    print("-" *len(title))

#key-value printer
def print_kv(label, value, width=20):
    print(f"{label.ljust(width)} : {value}")


def print_file_metrics(file_metrics):
    print_section("File Metrics")
    print_kv("Total files", file_metrics["total"])
    print_kv("Total lines", file_metrics["total_lines"])
    print_kv("Average lines/file", round(file_metrics["average_lines"], 2))
    print_kv("Largest file", file_metrics["largest_file"])
