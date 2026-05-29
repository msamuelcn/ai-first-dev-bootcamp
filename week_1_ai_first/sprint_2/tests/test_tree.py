import subprocess
import sys
import os

ROOT_TEST_FOLDER = "codeinsight/"


def run_cli(args):
    run_env = os.environ.copy()
    run_env.pop("CODEINSIGHT_MCP_SERVER_COMMAND", None)
    run_env.setdefault("CODEINSIGHT_MCP_TIMEOUT_SECONDS", "45")

    return subprocess.run(
        [sys.executable, ROOT_TEST_FOLDER + "main.py"] + args,
        capture_output=True,
        text=True,
        env=run_env,
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
