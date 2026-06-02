from pathlib import Path


def load_markdown_files(folder: str):
    files = []

    for ext in ["*.md", "*.mdx"]:
        files.extend(Path(folder).rglob(ext))

    documents = []

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            documents.append({"path": str(file), "text": f.read()})

    return documents
