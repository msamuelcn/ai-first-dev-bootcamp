import subprocess


def run_cmd(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def test_find_errors_valid_log():
    result = run_cmd(["python", "main.py", "find-errors", "logs/app.log"])

    assert result.returncode == 0
    assert "Errors Found" in result.stdout


def test_find_errors_clean_log(tmp_path):
    log = tmp_path / "clean.log"
    log.write_text("INFO: system running fine")

    result = run_cmd(["python", "main.py", "find-errors", str(log)])

    assert "0" in result.stdout or "No errors" in result.stdout


def test_find_errors_malformed_log(tmp_path):
    log = tmp_path / "bad.log"
    log.write_text("?????? #### RANDOM TEXT $$$$")

    result = run_cmd(["python", "main.py", "find-errors", str(log)])

    assert result.returncode == 0
