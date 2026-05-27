import subprocess

ROOT_TEST_FOLDER = "codeinsight/"


def run_cmd(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def test_analyze_valid_folder():
    result = run_cmd(["python", ROOT_TEST_FOLDER + "main.py", "analyze", "."])

    assert result.returncode == 0
    assert "FILE ANALYSIS SUMMARY" in result.stdout


def test_analyze_invalid_path():
    result = run_cmd(
        ["python", ROOT_TEST_FOLDER + "main.py", "analyze", "./does_not_exist"]
    )

    assert "Path not found" in result.stdout
    assert result.returncode == 0


def test_analyze_empty_folder(tmp_path):
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    result = run_cmd(
        ["python", ROOT_TEST_FOLDER + "main.py", "analyze", str(empty_dir)]
    )

    assert "FILE ANALYSIS SUMMARY" in result.stdout
