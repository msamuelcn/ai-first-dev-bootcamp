# Code Insight CLI

Code Insight CLI is a Python command-line tool for inspecting local projects and files through a real MCP filesystem server over stdio.

It is designed for developer workflows such as:
- project structure analysis
- file summarization
- source code explanation
- log error pattern scanning

## Features

- Analyze a project directory and detect file-type distribution
- Display a readable tree view of a directory
- Summarize text files with concise stats and purpose hints
- Explain source files with purpose, key symbols, and flow summary
- Scan log files for common error patterns and show grouped counts

## Installation

### Prerequisites

- Python 3.10+
- Node.js 18+ (required to run the filesystem MCP server via `npx`)

### Setup

1. Move into the sprint folder:

```bash
cd week_1_ai_first/sprint_2
```

2. (Optional but recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Optional: configure MCP root directory (defaults to current directory):

Windows PowerShell:

```powershell
$env:CODEINSIGHT_MCP_ROOT = "C:/Users/marks/OneDrive/Documents/AIWednesday/GauntletAI"
```

macOS/Linux:

```bash
export CODEINSIGHT_MCP_ROOT=/path/to/project
```

## Usage

Run commands from inside the codeinsight folder:

```bash
cd codeinsight
python main.py --help
```

General pattern:

```bash
python main.py <command> <path>
```

## Commands

### analyze

Analyze a project directory and print:
- total files
- file-type counts
- detected project type (FastAPI, Node.js, or generic Python)

```bash
python main.py analyze .
python main.py analyze ../
```

### summarize

Summarize a text file with concise output.

```bash
python main.py summarize ./main.py
python main.py summarize ../SPEC.md
```

### explain

Explain a source file in human-readable terms:
- purpose
- main functions/classes
- flow summary

```bash
python main.py explain ./commands/explain.py
python main.py explain ./commands/analyze.py
```

### tree

Show a readable directory tree.

```bash
python main.py tree .
python main.py tree ../
```

### find-errors

Scan a log file for key patterns:
- ERROR
- WARNING
- EXCEPTION
- TRACEBACK

Output includes grouped counts and top frequent issues.

```bash
python main.py find-errors ./app.log
python main.py find-errors ../logs/server.log
```

## Known Limitations

- MCP operations currently target filesystem tools only.
- No remote repository integration.
- Extremely large files may be slow to process.
- Summaries and explanations are heuristic-based and may miss deeper context.
- Log scanning uses pattern matching, not full semantic root-cause analysis.

## MCP Proof Notes

- Commands use an external process: `npx -y @modelcontextprotocol/server-filesystem <root>`.
- During command execution, the CLI initializes an MCP session and calls tools such as `list_directory` and `read_file`.
- If the external server is unavailable, commands fail with MCP connection errors instead of silently falling back to local in-process file reads.
- Set `CODEINSIGHT_MCP_TRACE=1` to print a visible request/response trace to stderr for reviewer evidence.
- Core commands such as `summarize` and `tree` depend on the MCP server for successful execution.

## Error Handling

The CLI is designed to fail gracefully with actionable messages for:
- invalid path format
- missing paths
- permission issues
- unsupported file types
- empty files
- MCP connection and operation errors

Stack traces are intentionally not shown in user-facing output.
