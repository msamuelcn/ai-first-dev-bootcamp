from pathlib import Path

documents = []

for ext in ["*.md", "*.mdx"]:
    for file in Path("../corpus/streamlit").rglob(ext):
        documents.append(file)
        print(f"Found document: {file}")

print(f"Found {len(documents)} documents")
