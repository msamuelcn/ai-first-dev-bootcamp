import os
import subprocess

ROOT_TEST_FOLDER = "codeinsight/"


def run_cmd(cmd, env=None):
    run_env = os.environ.copy()
    run_env.pop("CODEINSIGHT_MCP_SERVER_COMMAND", None)
    run_env.setdefault("CODEINSIGHT_MCP_TIMEOUT_SECONDS", "45")
    if env:
        run_env.update(env)

    return subprocess.run(cmd, capture_output=True, text=True, env=run_env)


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
        ["python", ROOT_TEST_FOLDER + "main.py", "analyze", str(empty_dir)],
        env={"CODEINSIGHT_MCP_ROOT": str(tmp_path)},
    )

    assert "FILE ANALYSIS SUMMARY" in result.stdout
