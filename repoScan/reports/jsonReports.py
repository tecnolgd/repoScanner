#json.py --> to generate metrics in a machine-readable format

import json
import os
from datetime import datetime

def write_json_report(metrics, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "metrics": metrics
    }

    path = os.path.join(output_dir, "report.json")

    with open(path, "w") as f:
        json.dump(report, f, indent=4)

    return path