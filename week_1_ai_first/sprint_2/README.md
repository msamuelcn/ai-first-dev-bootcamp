# Code Insight CLI

Code Insight CLI is a Python command-line tool for inspecting local projects and files through an MCP-style filesystem client layer.

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

## Usage

Run commands from inside the code-insight folder:

```bash
cd code-insight
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

- Current implementation uses a local filesystem transport adapter for MCP-style operations.
- No remote repository integration.
- Extremely large files may be slow to process.
- Summaries and explanations are heuristic-based and may miss deeper context.
- Log scanning uses pattern matching, not full semantic root-cause analysis.

## Error Handling

The CLI is designed to fail gracefully with actionable messages for:
- invalid path format
- missing paths
- permission issues
- unsupported file types
- empty files
- MCP connection and operation errors

Stack traces are intentionally not shown in user-facing output.
