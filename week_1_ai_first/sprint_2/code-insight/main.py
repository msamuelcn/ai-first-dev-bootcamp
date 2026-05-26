"""Entrypoint for the Code Insight CLI."""

from cli import run


def main() -> int:
	"""Run the CLI application."""
	return run()


if __name__ == "__main__":
	raise SystemExit(main())
