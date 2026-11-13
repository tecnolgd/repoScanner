import sys

from repoScan.cli import main


def test_unknown_option_after_path(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)
    option = "--definitely-invalid"
    monkeypatch.setattr(sys, "argv", ["reposcan", str(tmp_path), option])

    try:
        main()
    except SystemExit as exc:
        status = exc.code
    else:
        status = 0

    assert status not in (0, None), "CLI accepted an unknown option"
    assert option in capsys.readouterr().err
    assert not (tmp_path / "output" / "report.json").exists()
