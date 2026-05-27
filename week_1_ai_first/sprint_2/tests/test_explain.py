import subprocess

ROOT_TEST_FOLDER = "codeinsight/"


def run_cmd(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def test_explain_valid_file():
    result = run_cmd(
        [
            "python",
            ROOT_TEST_FOLDER + "main.py",
            "explain",
            ROOT_TEST_FOLDER + "main.py",
        ]
    )

    assert result.returncode == 0
    assert "Purpose" in result.stdout or "File" in result.stdout


def test_explain_invalid_file():
    result = run_cmd(["python", ROOT_TEST_FOLDER + "main.py", "explain", "fake.py"])

    assert "not found" in result.stdout.lower()


def test_explain_empty_file(tmp_path):
    f = tmp_path / "empty.py"
    f.write_text("")

    result = run_cmd(["python", ROOT_TEST_FOLDER + "main.py", "explain", str(f)])

    assert "empty" in result.stdout.lower()
