import sys
from unittest.mock import Mock

import pytest

from repoScan import cli


@pytest.mark.parametrize("option", ["--definitely-invalid", "--sttas", "-x", "---raw"])
def test_unknown_option_after_path(monkeypatch, tmp_path, capsys, option):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["reposcan", str(tmp_path), option])
    scan = Mock(return_value=[])
    monkeypatch.setattr(cli, "dir_scanner", scan)

    try:
        cli.main()
    except SystemExit as exc:
        status = exc.code
    else:
        status = 0

    assert status == 2, "CLI accepted an unknown option"
    assert option in capsys.readouterr().err
    scan.assert_not_called()
    assert not (tmp_path / "output" / "report.json").exists()


@pytest.mark.parametrize("args", [
    ["missing"], [")"], [","], ["&"], ["x"],
    ["repo", "."], [".", "repo"], [".", "."], ["repo", "--stats", "."],
])
def test_invalid_positional_paths(monkeypatch, tmp_path, capsys, args):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "repo").mkdir()
    monkeypatch.setattr(sys, "argv", ["reposcan", *args])
    scan = Mock(return_value=[])
    monkeypatch.setattr(cli, "dir_scanner", scan)

    with pytest.raises(SystemExit) as exc:
        cli.main()

    assert exc.value.code == 2
    assert "Error:" in capsys.readouterr().err
    scan.assert_not_called()
    assert not (tmp_path / "output" / "report.json").exists()


@pytest.mark.parametrize(("args", "root", "expected"), [
    ([], ".", "STATS/SUMMARY"),
    (["--raw", "a--project"], "a--project", "RAW/DEVELOPER"),
    (["+--lc", "--dev"], "+--lc", "RAW/DEVELOPER"),
    (["--stats", "."], ".", "STATS/SUMMARY"),
    (["--nerd", ".hidden"], ".hidden", "STATS/SUMMARY"),
    (["./relative", "--max"], "./relative", "Largest file:"),
    (["--tbytes", "repo"], "repo", "Total bytes:"),
    (["./-repo", "--sort"], "./-repo", "Sorted Directory"),
    (["--search", "example.txt", "."], ".", "File found: example.txt"),
    (["--lc", "example.txt"], ".", "Line count of example.txt: 2"),
])
def test_valid_scan(monkeypatch, tmp_path, capsys, args, root, expected):
    monkeypatch.chdir(tmp_path)
    (tmp_path / root).mkdir(exist_ok=True)
    (tmp_path / root / "example.txt").write_text("one\ntwo\n")
    scan = Mock(wraps=cli.dir_scanner)
    monkeypatch.setattr(cli, "dir_scanner", scan)
    monkeypatch.setattr(sys, "argv", ["reposcan", *args])

    cli.main()

    scan.assert_called_once_with(root)
    assert expected in capsys.readouterr().out
    assert (tmp_path / "output" / "report.json").is_file()


@pytest.mark.parametrize("flag", ["-h", "--help"])
def test_help(monkeypatch, tmp_path, capsys, flag):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["reposcan", flag])
    with pytest.raises(SystemExit) as exc:
        cli.main()
    assert exc.value.code == 0
    assert "USAGE:" in capsys.readouterr().out
    assert not (tmp_path / "output" / "report.json").exists()
