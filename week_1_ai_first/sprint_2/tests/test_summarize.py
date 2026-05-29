import subprocess
import sys
import os

ROOT_TEST_FOLDER = "codeinsight/"


def run_cli(args, env=None):
    run_env = os.environ.copy()
    if env:
        run_env.update(env)

    return subprocess.run(
        [sys.executable, ROOT_TEST_FOLDER + "main.py"] + args,
        capture_output=True,
        text=True,
        env=run_env,
    )


def test_summarize_valid_file():
    result = run_cli(["summarize", ROOT_TEST_FOLDER + "main.py"])

    assert result.returncode == 0
    assert result.stdout != ""
    assert "file" in result.stdout.lower() or "summary" in result.stdout.lower()


def test_summarize_empty_file(tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    result = run_cli(
        ["summarize", str(empty_file)],
        env={"CODEINSIGHT_MCP_ROOT": str(tmp_path)},
    )

    assert result.returncode == 0
    assert "empty" in result.stdout.lower()


def test_summarize_invalid_file():
    result = run_cli(["summarize", "does_not_exist.txt"])

    assert result.returncode == 0
    assert "not found" in result.stdout.lower() or "error" in result.stdout.lower()
