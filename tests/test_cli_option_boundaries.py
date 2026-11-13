import sys
from unittest.mock import Mock

import pytest

from repoScan import cli


def run_cli(monkeypatch, args):
    monkeypatch.setattr(sys, "argv", ["reposcan", *args])
    try:
        cli.main()
    except SystemExit as exc:
        return exc.code
    return 0


@pytest.mark.parametrize(("args", "problem"), [
    (["=--stats"], "=--stats"),
    (["+--lc"], "+--lc"),
    (["---raw"], "---raw"),
    ([".--help"], ".--help"),
    (["@--sort"], "@--sort"),
    (["x--nerd"], "x--nerd"),
    (["+-h"], "+-h"),
    (["repo", "=", "--stats"], "="),
    (["+", "--stats", "repo"], "+"),
    (["repo", "-", "--stats"], "-"),
    ([".", "repo", "--stats"], "repo"),
    (["--lc", "--stats"], "--lc"),
])
def test_malformed_arguments(monkeypatch, tmp_path, capsys, args, problem):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "repo").mkdir()
    scan = Mock(return_value=[])
    monkeypatch.setattr(cli, "dir_scanner", scan)

    assert run_cli(monkeypatch, args) == 2
    assert problem in capsys.readouterr().err
    scan.assert_not_called()
    assert not (tmp_path / "output" / "report.json").exists()


@pytest.mark.parametrize(("args", "root", "expected"), [
    ([], ".", "STATS/SUMMARY"),
    ([".", "--stats"], ".", "STATS/SUMMARY"),
    (["--nerd", "./relative"], "./relative", "STATS/SUMMARY"),
    (["./.--stats", "--dev"], "./.--stats", "RAW/DEVELOPER"),
    (["--raw", "a--project"], "a--project", "RAW/DEVELOPER"),
    (["--lc", "example.txt", ".hidden"], ".hidden", "Line count of example.txt: 2"),
])
def test_valid_scan(monkeypatch, tmp_path, capsys, args, root, expected):
    monkeypatch.chdir(tmp_path)
    (tmp_path / root).mkdir(exist_ok=True)
    (tmp_path / "example.txt").write_text("one\ntwo\n")
    scan = Mock(wraps=cli.dir_scanner)
    monkeypatch.setattr(cli, "dir_scanner", scan)

    assert run_cli(monkeypatch, args) == 0
    scan.assert_called_once_with(root)
    assert expected in capsys.readouterr().out
    assert (tmp_path / "output" / "report.json").is_file()


@pytest.mark.parametrize("flag", ["-h", "--help"])
def test_help(monkeypatch, tmp_path, capsys, flag):
    monkeypatch.chdir(tmp_path)
    assert run_cli(monkeypatch, [flag]) == 0
    assert "USAGE:" in capsys.readouterr().out
    assert not (tmp_path / "output" / "report.json").exists()
