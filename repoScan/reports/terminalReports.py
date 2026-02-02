#terminalReports.py

#section printer
def print_section(title):
    print("\n" + title)
    print("-" *len(title))

#key-value printer
def print_kv(label, value, width=20):
    print(f"{label.ljust(width)} : {value}")

