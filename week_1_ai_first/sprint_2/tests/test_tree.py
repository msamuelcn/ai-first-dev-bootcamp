import subprocess
import sys

ROOT_TEST_FOLDER = "codeinsight/"


def run_cli(args):
    return subprocess.run(
        [sys.executable, ROOT_TEST_FOLDER + "main.py"] + args,
        capture_output=True,
        text=True,
    )


def test_tree_valid_path():
    result = run_cli(["tree", "."])

    assert result.returncode == 0
    assert result.stdout != ""
    assert "Error" not in result.stdout


def test_tree_invalid_path():
    result = run_cli(["tree", "./path_that_does_not_exist"])

    assert result.returncode == 0
    assert "not found" in result.stdout.lower() or "error" in result.stdout.lower()


def test_tree_empty_input():
    result = run_cli(["tree", ""])

    assert result.returncode == 0
    assert "error" in result.stdout.lower()
