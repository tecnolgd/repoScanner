<!--Roadmap for repoScanner-->

## ✓ Completed

-  JSON export with machine-readable reports
-  Terminal reporting (stats & raw modes)
-  Extended language support (40+ languages including JavaScript, Go, Rust, and more)
-  Added wrapper script for fast scanning
-  Added Benchmarking suite
-  Included text-based sample outputs  
-  Optional native `libcvault` submodule integration for advanced CLI utilities
-  Added a shared wrapper for `libcvault` and transparent Python fallback when the native module is unavailable
-  Cached directory scanning per root path to avoid redundant rescans
-  PyPI packaging with multi-platform wheel builds (Linux, macOS, Windows)
-  CI/CD publish workflow with `cibuildwheel` for end-user distribution

## Coming Soon

- HTML report generation
- Gitignore integration for smarter scanning
- Circular dependency detection
- Auto-detect and scan Repositories
- Improved UI and formatting
- Performance optimization for large repositories
- Optional incremental or changed-file scanning for very large repositories
