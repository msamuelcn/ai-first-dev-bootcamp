# SPEC.md

# Sprint 2 - MCP Filesystem CLI Tool

## Project Title

Code Insight CLI

---

# Objective
Build a command-line interfact (CLI) tool that uses a Model Control Plane (MCP) filesystem serve to analyze and inspect local project files.

The tool should help developers:
 - inspect directory structures
 - summarize files
 - explain source code files
 - identify potential issues in code or error patterns in log files

The application must use MCP integration for filesystem access instead of directly accessing the files through standard Python file handling for core features.

---

# Primary Goals
 - Demonstrate understanding of MCP integration
 - Build a usable CLI developer tool
 - Implement safe and readable error handling
 - Use AI-assisted development responsibly
 - Maintain clear documentation, AI interaction logs, and code comments

---

# Tech Stack
 - Python 3.10+
 - argparse (for CLI handling)
 - MCP Python SDK (for filesystem access) / MCP Client
 - Git
 - Github
 - Claude Code or Github Copilot (for AI-assisted development)
 - Pytest (for testing)

---

# MCP Integration

## MCP Server

Filesystem MCP Server

## Purpose

The MCP server will provide:
 - directory listing
 - file content retrieval
 - project structure analysis

## MCP Operations Used
 - list_directory(path)
 - read_file(path)
 - analyze_project(path)
 - get_file_metadata(path)

---

# Core Commands

## 1. analyze
### Command
```bash
code-insight analyze <path>
```
### Description
Analyzes a directory structure and outputs:
 - total files
 - detected file types
 - possible project type
 - high-level summary of project structure

### Example
```bash
code-insight analyze /path/to/project
```

## 2. summarize
### Command
```bash
code-insight summarize <file>
```
### Description
Reads a file through MCP and outputs:
 - short summary
 - estimated purpose
 - important sections detected

### Example
```bash
code-insight summarize /path/to/file
```

## 3. explain
### Command
```bash
code-insight explain <file>
```
### Description
Explains the purpose of a source code file in human-readable format.
 - key functions/classes
 - overall purpose
 - potential issues or code smells

### Example
```bash
code-insight explain /path/to/file
```

## 4. tree
### Command
```bash
code-insight tree <path>
```
### Description
Displays the directory structure of a project in a tree-like format.
 - hierarchical view of files and directories
 - easy navigation of project structure
 - quick overview of project organization


### Example
```bash
code-insight tree /path/to/project
```

## 5. find-errors
### Command
```bash
code-insight find-errors <path>
```
### Description
Finds potential errors in a project by analyzing files and logs.
 - Scan log files for:
   - ERROR
   - EXCEPTION
   - WARNING
   - Traceback patterns
 - identifies common error patterns
 - highlights suspicious code sections
 - provides suggestions for fixes

Outputs a summarized report.

### Example
```bash
code-insight find-errors logs/app.log
```

# Functional Requirements

The system must:
 - support all listed commands
 - use MCP integration for filesystem access
 - return readable CLI output
 - validate command arguments
 - fail gracefully with actionable messages
 - avoid exposing raw stack traces to users

# Non-Functional Requirements
The system should:

 - be modular and readable
 - have clear CLI formatting
 - use meaningful command names
 - maintain simple architecture
 - avoid unnecessary dependencies

# Error Handling Requirements
 - Invalid Path: "Error: Path not found: <path>. Please check the path and try again."
 - Unsupported File Type: "Error: Unsupported file type for analysis: <file>. Supported types are .py, .js, .log, etc."
 - MCP Errors: "Error: MCP operation failed: <error message>. Please check your MCP connection and try again."
 - MCP Connection Failure: "Error: Unable to connect to MCP server. Please ensure the server is running and try again."
 - Empty File: "Error: File is empty and cannot be summarized: <file>. Please provide a valid file for analysis."
 - Permission Denied: "Error: Permission denied when accessing: <path>. Please check your permissions and try again."
 - Invalid Path Format: "Error: Invalid path format: <path>. Please provide a valid path and try again."

# Output Requirements
Define:
 - clean CLI output
 - structured formatting
 - clear error messages

# Constraints
 - max 5 commands
 - no external APIs (unless required)
 - must use MCP for at least 1 core feature

# AI Development Workflow
The project will follow an AI-first workflow:
1. Write specification before implementation
2. Generate code incrementally using AI tools
3. Validate all generated code manually
4. Add error handling manually if needed
5. Log all AI interactions
6. Commit changes incrementally

# AI Interaction Logging
An AI_LOG.md file will contain:
 - prompts used
 - generated outputs
 - accepted changes
 - rejected suggestions
 - manual fixes
 - validation decisions

# Repository Structure
```
project/
│
├── code-insight/
│   ├── main.py
│   ├── commands/
│   ├── mcp/
│   ├── utils/
│
├── tests/
│
├── README.md
├── SPEC.md
├── AI_LOG.md
├── requirements.txt
```

# README Requirements
README must include:
 - project overview
 - installation instructions
 - command examples
 - architecture explanation
 - known limitations

# Known Limitations
Initial version limitations:
 - only supports local filesystem MCP server
 - no remote GitHub integration
 - limited handling for extremely large files
 - summaries are heuristic-based and may be incomplete

# Success Criteria
The sprint is considered complete when:
 - all commands function correctly
 - MCP integration works
 - README is complete
 - SPEC.md is committed before implementation
 - AI interaction logs are complete
 - peer review comments are addressed
 - demo is ready and runnable

# Out of Scope
The following are intentionally excluded:
 - authentication
 - cloud deployment
 - database storage
 - GUI interface
 - multi-user support
 - real-time monitoring
 - advanced AI agent orchestration


