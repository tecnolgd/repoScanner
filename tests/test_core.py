import os
from pathlib import Path

from repoScan.analyzer.dependencyAnalyzer import dependency_analyzer
from repoScan.analyzer.sizeAnalyzer import size_analyzer
from repoScan.analyzer.structureAnalyzer import structure_analyzer
from repoScan.scanner.dirScanner import dir_scanner
from repoScan.scanner.metrics import generate_metrics
from repoScan.utility.helpers import extract_c_includes, extract_python_imports


def _write_file(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_python_imports():
    lines = [
        "import os",
        "import sys, json",
        "from pathlib import Path",
        "from app.config import settings",
        "# comment line",
    ]

    imports = extract_python_imports(lines)

    assert set(imports) == {"os", "sys", "json", "pathlib", "app.config"}


def test_extract_includes_():
    lines = [
        '#include <iostream>',
        '#include "config.hpp"',
        '#include <vector>',
        "int main() { return 0; }",
    ]

    includes = extract_c_includes(lines)

    assert set(includes) == {"iostream", "vector"}


def test_dependency_analyzer(tmp_path):
    py_file = _write_file(
        tmp_path / "app" / "main.py",
        "import os\nfrom pathlib import Path\nfrom app.config import settings\n",
    )
    c_file = _write_file(
        tmp_path / "native" / "parser.hpp",
        '#include <vector>\n#include <string>\n#include "config.hpp"\n',
    )

    report = dependency_analyzer([str(py_file), str(c_file)])

    assert set(report[str(py_file)]) == {"os", "pathlib", "app.config"}
    assert set(report[str(c_file)]) == {"vector", "string"}


def test_size_analyzer_(tmp_path):
    one = _write_file(tmp_path / "alpha.txt", "one\ntwo\n")
    two = _write_file(tmp_path / "beta.txt", "three\nfour\nfive\n")

    report = size_analyzer([str(one), str(two)])

    assert report["total_files"] == 2
    assert report["total_lines"] == 5
    assert report["total_bytes"] == one.stat().st_size + two.stat().st_size
    assert report["average_lines"] == 2
    assert report["average_file_size"] == report["total_bytes"] // 2
    assert len(report["largest_files"]) == 2


def test_structure_analyzer_(tmp_path):
    nested_dir = tmp_path / "src" / "pkg"
    one = _write_file(nested_dir / "module.py", "print('hello')\n")
    two = _write_file(tmp_path / "root.txt", "a\nb\n")

    report = structure_analyzer([str(one), str(two)])

    assert report["total_files"] == 2
    assert str(nested_dir) in report["directories"]
    assert str(tmp_path) in report["directories"]
    assert report["max_depth"] > 0
    assert report["files/directory"][str(tmp_path)] == 1
    assert report["files/directory"][str(nested_dir)] == 1


def test_dir_scanner_list(tmp_path):
    nested = tmp_path / "pkg"
    nested.mkdir()
    first = _write_file(tmp_path / "root.py", "print('root')\n")
    second = _write_file(nested / "child.py", "print('child')\n")

    scanned = sorted(dir_scanner(str(tmp_path)))

    assert scanned == sorted([str(first), str(second)])


def test_generate_metrics_(tmp_path):
    py_file = _write_file(
        tmp_path / "demo.py",
        "import os\nfrom pathlib import Path\n",
    )
    h_file = _write_file(
        tmp_path / "header.hpp",
        '#include <vector>\n#include <string>\n',
    )

    size_report = size_analyzer([str(py_file), str(h_file)])
    dep_report = dependency_analyzer([str(py_file), str(h_file)])
    metrics = generate_metrics([str(py_file), str(h_file)], size_report, dep_report)

    assert metrics["file_metrics"]["total"] == 2
    assert metrics["dependency_metrics"]["total"] >= 3
    assert metrics["language_metrics"]["Python"] == 1
    assert metrics["language_metrics"]["C++"] == 1
