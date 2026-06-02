from chunking import smart_chunk
from doc_loader import load_markdown_files

docs = load_markdown_files("corpus")

all_chunks = []

for doc in docs[:1]:
    chunked = smart_chunk(doc)
    print(f"Document: {doc['path']} - Chunks: {len(chunked)}")
    print(chunked)  # Print the first chunk for inspection
    all_chunks.extend(chunked)

print("Chunks created:", len(all_chunks))
