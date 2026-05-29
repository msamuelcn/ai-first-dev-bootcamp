# AI Interaction Log

This file tracks key prompts, AI outputs, and implementation decisions for Sprint 2.

## Session 1
### Prompt
"Based on SPEC.md, suggest a clean Python project structure for the CLI tool using argparse and MCP integration. Keep architecture simple and modular."

### AI Output (Summary)
Suggested a modular Python structure with a CLI entry point, command modules, and helper layers.

### Actions Taken
- Created project directory structure for the CLI tool.
- Added a `main.py` entry point.
- Created command files for `analyze`, `summarize`, `explain`, `tree`, and `find_errors`.

---

## Session 2
### Prompt
"Create a basic argparse CLI skeleton for the Code Insight CLI project. Commands: analyze, summarize, explain, tree, find-errors. Only create command registration and placeholder handlers. Do not implement business logic yet."

### AI Output (Summary)
Provided argparse-based CLI skeleton with subcommand registration and placeholder handlers.

### Actions Taken
- Implemented command registration for all 5 commands.
- Wired placeholder handlers for incremental implementation.

---

## Session 3
### Prompt
"Create a reusable MCP client module for communicating with a filesystem MCP server. Requirements: connect to MCP server, expose helper methods, separate connection logic from CLI commands, include basic exception handling."

### AI Output (Summary)
Provided reusable MCP client design with connection lifecycle, helper methods, and exception handling.

### Actions Taken
- Added generic MCP client lifecycle and error classes.
- Added `FilesystemMCPClient` helper methods:
  - `list_directory(path)`
  - `read_file(path)`
  - `analyze_project(path)`
  - `get_file_metadata(path)`
- Exported MCP interfaces for reuse.

---

## Session 4
### Prompt
"Implement the 'tree' command using the MCP client. Requirements: list directory contents, display readable tree format, handle invalid paths gracefully, do not expose stack traces."

### AI Output (Summary)
Implemented MCP-backed tree command with readable output and safe error handling.

### Actions Taken
- Implemented directory listing via MCP client.
- Added recursive tree rendering.
- Added user-safe error paths for invalid path and MCP failures.

---

## Session 5
### Prompt
"Refactor the tree command error handling. Requirements: user-friendly errors, no raw exceptions, actionable guidance for invalid paths."

### AI Output (Summary)
Refactored error handling into centralized message mapping and removed raw exception details.

### Actions Taken
- Added `_format_tree_error(path, error)` mapper.
- Improved guidance for invalid path formats.
- Ensured fallback behavior remains graceful and readable.

---

## Session 6
### Prompt
"Implement the summarize command using MCP read_file functionality. Requirements: summarize text files, detect empty files, reject unsupported binary files, keep output concise."

### AI Output (Summary)
Implemented MCP-backed summarize flow with empty/binary checks and concise summary output.

### Actions Taken
- Added `read_file` support in local MCP filesystem transport.
- Implemented concise summarize output format.
- Added empty-file and unsupported-file handling.

---

## Session 7
### Prompt
"Implement the 'analyze' CLI command. Requirements: folder path input, recursive listing via MCP, file type counts, project-type detection (FastAPI/Node.js/generic Python), clean summary. Constraints: no direct filesystem access in command, MCP only, handle invalid path gracefully."

### AI Output (Summary)
Implemented analyze command with recursive MCP listing, file-type statistics, and project-type heuristics.

### Actions Taken
- Added recursive file flattening from MCP payload.
- Counted file extensions and summarized totals.
- Added FastAPI/Node.js/generic Python detection heuristics.
- Added user-friendly invalid-path handling.

---

## Session 8
### Prompt
"Implement the 'explain' command. Requirements: file input, MCP read_file usage, human-readable explanation including purpose, main functions/classes, and flow summary. Constraints: handle empty/unsupported files, no raw file dump, no stack traces."

### AI Output (Summary)
Implemented source explanation command with structure-aware summary and safe output.

### Actions Taken
- Parsed source files for symbol extraction.
- Added purpose and flow inference heuristics.
- Enforced empty-file and unsupported-type guards.
- Prevented raw file content dumping.

---

## Session 9
### Prompt
"Implement 'find-errors' CLI command. Requirements: log file input, MCP read, detect ERROR/WARNING/Exception/Traceback, grouped summary, counts, top 3 frequent issues. Constraints: must not crash on malformed logs, must not show raw stack traces, output must be summarized and readable."

### AI Output (Summary)
Implemented log scanner with pattern detection, grouped counts, issue frequency ranking, and robust malformed-log handling.

### Actions Taken
- Added pattern detection for required keywords.
- Added grouped output and top-3 issue reporting.
- Added sanitization to avoid stack trace dumps.
- Ensured resilient parsing on malformed input.

---

## Session 10
### Prompt
"Review current CLI architecture and suggest refactoring opportunities to reduce duplication while keeping the design simple."

### AI Output (Summary)
Suggested reducing duplication through shared helpers for client initialization, error formatting, and output formatting.

### Actions Taken
- Documented refactor opportunities for future cleanup.

---

## Session 11
### Prompt
"Generate a README draft for the Code Insight CLI tool. Include installation, usage, command examples, known limitations."

### AI Output (Summary)
Generated complete README draft covering required sections.

### Actions Taken
- Added README content with installation, usage, examples, and limitations.

---

## Session 12
### Prompt
"Can you review the packages imported, list them in requirements.txt, and install?"

### AI Output (Summary)
Reviewed imports and updated requirements for project use and testing.

### Actions Taken
- Updated `requirements.txt`.
- Installed dependencies with `pip install -r requirements.txt`.

---

## Session 13
### Prompt
"Can you create scenarios that will log errors? I want to appreciate find-errors and how it will work."

### AI Output (Summary)
Created multiple log scenarios to demonstrate pattern detection and summarization behavior.

### Actions Taken
- Added sample scenario logs for ERROR/WARNING/Exception/Traceback/malformed/clean cases.
- Executed `find-errors` across scenarios to validate behavior.

---

## Session 14
### Prompt
```text
pytest tests/test_mcp_filesystem.py

def test_mcp_connection():

E ModuleNotFoundError: No module named 'codeinsight'

tests\test_mcp_filesystem.py:2: ModuleNotFoundError
=========================================== short test summary info ===========================================
FAILED tests/test_mcp_filesystem.py::test_mcp_connection - ModuleNotFoundError: No module named 'codeinsight'
============================================== 1 failed in 2.46s ==============================================
```

### AI Output (Summary)
Diagnosed import resolution issue and path/package visibility mismatch for pytest context.

### Actions Taken
- Updated test import strategy and adjusted setup so test module resolves project package correctly.

---
## Session 15

### Issue
Received feedback that the project is not yet MCP-proven, as it relies on a local filesystem adapter rather than demonstrating real MCP server consumption.

```
Sprint 2 is MCP-shaped, not yet MCP-proven

The curriculum requires “a CLI tool that consumes at least one MCP server.”

The attempt has an MCPClient, MCPTransport, and LocalFilesystemTransport, but its core behavior is local filesystem access through a custom adapter. That is useful as a pedagogical abstraction, but it is not yet strong evidence of real MCP server consumption.

A strict reviewer will ask the Week 1 defense question: “What does the MCP protocol actually do under the hood? Explain it without acronyms.” The current repo does not yet provide enough protocol-level evidence to survive that question.
```

### Prompt

```
I have this in my received  review. Can you explain it more? And give examples if possible. What files I should change or modify?


Sprint 2 is MCP-shaped, not yet MCP-proven

The curriculum requires “a CLI tool that consumes at least one MCP server.”

The attempt has an MCPClient, MCPTransport, and LocalFilesystemTransport, but its core behavior is local filesystem access through a custom adapter. That is useful as a pedagogical abstraction, but it is not yet strong evidence of real MCP server consumption.

A strict reviewer will ask the Week 1 defense question: “What does the MCP protocol actually do under the hood? Explain it without acronyms.” The current repo does not yet provide enough protocol-level evidence to survive that question.
```

### AI Output (Summary)
 - Findings:
    - I found the project layout; next I’m reading the MCP client and transport implementation to show exactly why the review calls it MCP-shaped.
    - Confirmed the key gap: the transport currently never talks to an external server process.
    - I confirmed there is no real MCP dependency configured.
    - You designed your code to look like an MCP integration, but you have not yet demonstrated real server communication.
    - Why they said “MCP-shaped, not MCP-proven”
     - The transport class is local logic, not a server client: filesystem.py:11, filesystem.py:46.
     - Open/close do nothing, so no external process/session is established: filesystem.py:38.
     - Factory returns that local transport directly: filesystem.py:176.
     - All core commands use that same local factory, so all features run without a real server: tree.py:10, summarize.py:9, analyze.py:11, explain.py:11, find_errors.py:11.
     - Dependencies do not show an MCP SDK/server client package: requirements.txt, pyproject.toml
     - Your README already admits this limitation: README.md:133.
     - Current MCP test only checks object creation, not real server tool calls: test_mcp_filesystem.py:9

### Actions Taken
 - Asked AI to give me examples of how to make it MCP-proven. Also asked for a minimal acceptance checklist to ensure the next iteration is MCP-proven.
  - AI provided examples of how to implement a real MCP server and client interaction, along with a checklist for MCP-proven status.

---
## Session 16
### Prompt
```
"If you want, I can next give you a minimal acceptance checklist you can hand to reviewers, with pass/fail criteria for “MCP-proven.”
Yes please
```

### AI Output
```
Great. Here is a minimal reviewer checklist you can use as a pass/fail gate for MCP-proven.

**MCP-Proven Acceptance Checklist (Pass/Fail)**

1. Real server process is used
- Pass: CLI starts or connects to an external filesystem server process during command execution.
- Fail: All file operations happen in local in-process code only.

2. Real request/response exchange is visible
- Pass: There is observable evidence (debug logs, trace output, or test capture) showing at least one tool request and one structured response.
- Fail: No evidence of message exchange, only function calls inside the app.

3. At least one core command depends on MCP
- Pass: At least one required command cannot complete without MCP server communication.
- Fail: Commands still work fully when MCP is removed because they directly read local files.

4. Connection lifecycle is implemented
- Pass: Connect, call, and disconnect are all exercised in normal flow.
- Fail: Open/close are no-ops or never used.

5. Error behavior proves network/process boundary
- Pass: User-facing errors clearly distinguish:
  - server unavailable
  - tool operation failure
  - invalid user input
- Fail: Errors are generic or identical to local filesystem exceptions only.

6. Tool coverage matches your claim
- Pass: You can demonstrate list directory and read file through MCP path at minimum.
- Fail: Claimed tools exist but are not actually invoked in runtime.

7. Tests verify protocol behavior, not object creation
- Pass: Automated tests assert successful server-backed call(s) and failure path(s).
- Fail: Tests only assert client object exists or flags default state.

8. Dependencies and setup are reproducible
- Pass: Required packages and setup steps for MCP server/client are documented and installable.
- Fail: No dependency/config evidence for real MCP usage.

9. README explains under-the-hood flow plainly
- Pass: README explains, in simple language, how the CLI sends a request to a separate server and receives results.
- Fail: README only says “MCP-style” or “MCP-shaped” with no concrete flow.

10. Demo script can be defended live
- Pass: You can run one command live and show:
  - server starts/connects
  - request sent
  - response received
  - user output rendered
- Fail: Demo only shows final output with no protocol-level proof.

**Quick Reviewer Scorecard**
- 9-10 pass: Clearly MCP-proven.
- 7-8 conditional pass: Good, but missing one proof artifact.
- 0-6 fail: Still MCP-shaped.

**Minimum evidence bundle to submit**
1. One terminal capture of a successful MCP-backed command.
2. One terminal capture of server-down failure with friendly error.
3. One automated test proving real MCP call path.
4. One README section “How it works under the hood” in plain language.

If you want, I can draft a one-page defense script you can read in under 2 minutes during review.
```
### Actions Taken
 - I started to ask for checklist # 1 and # 2, but I think I will need to implement the MCP server and client first to get those captures. So I will hold off on asking for the defense script until I have those pieces in place.

---
## Session 17
### Prompt
```
Example of how I can pass. What specific files I should add/edit. WHat server I should set up

1. Real server process is used

- Pass: CLI starts or connects to an external filesystem server process during command execution.
- Fail: All file operations happen in local in-process code only.

```

### AI Output
To pass the "Real server process is used" criterion, you will need to implement a simple MCP server that can handle filesystem operations, and modify your CLI to connect to this server instead of using local in-process code.

Recommended Server To Set Up
 - Use the official filesystem MCP server package: @modelcontextprotocol/server-filesystem.
 - Run it as an external process from your CLI using npx (stdio mode).
 - Give it one allowed root folder (your project root) so reviewers can see controlled access.

## What I did
1. Added a real stdio MCP transport that launches and calls the external filesystem server.
2. Made real MCP client the default for commands (instead of local in-process transport).
3. Exported new MCP factories/transports.
4. Added runtime dependency and test marker config.

---

## Session 18
### Prompt
"Apply the suggestion for fix to pass: Real request/response exchange is visible."

### AI Output (Summary)
Added opt-in MCP trace output so a terminal capture shows both the tool request and the structured response without changing normal CLI output.

### Actions Taken
- Added `CODEINSIGHT_MCP_TRACE=1` support to the stdio MCP transport.
- Emitted request and response trace lines to stderr for reviewer evidence.
- Added a regression test that captures trace output for one MCP tool call.
- Verified a live run of `python main.py summarize main.py` prints both trace lines and the final summary.

---
## Session 19
### Prompt
"Apply the suggestion for fix to pass: At least one core command depends on MCP."

### AI Output (Summary)
Documented and tested a core command dependency on MCP by forcing summarize to fail when the MCP connection setup is unavailable, confirming there is no local fallback path.

### Actions Taken
- Added a regression test in `tests/test_cli.py` that monkeypatches the MCP client factory to raise `MCPConnectionError`.
- Verified the summarize command prints the MCP connection error when the server cannot be reached.
- Kept the command flow dependent on the external filesystem server for normal execution.
