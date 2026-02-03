<!--Architecture details and breakdown for repoScanner-->

## Architecture Overview

scanner/     → File discovery & raw data extraction(including dependencies)
metrics.py   → Aggregation & derived metrics
analyzer/    → Structural and size analysis
reports/     → Terminal & JSON report generation 
cli.py       → Entry point and orchestration
output/      → JSON report output