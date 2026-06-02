def chunk_text(text, chunk_size=500, overlap=60):
    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]

        chunks.append(" ".join(chunk))

        start = end - overlap  # overlap helps context continuity

    return chunks


def chunk_markdown_with_headers(text, source_path):
    lines = text.split("\n")

    chunks = []
    current_header = None
    buffer = []

    for line in lines:
        if line.startswith("#"):
            # flush old chunk
            if buffer:
                chunks.append(
                    {
                        "header": current_header,
                        "text": "\n".join(buffer),
                        "source": source_path,
                    }
                )
                buffer = []

            current_header = line.strip()

        else:
            buffer.append(line)

    # last chunk
    if buffer:
        chunks.append(
            {"header": current_header, "text": "\n".join(buffer), "source": source_path}
        )

    return chunks


def smart_chunk(doc):
    header_chunks = chunk_markdown_with_headers(doc["text"], doc["path"])

    final_chunks = []

    for hc in header_chunks:
        sub_chunks = chunk_text(hc["text"])

        for sc in sub_chunks:
            final_chunks.append(
                {
                    "text": sc,
                    "metadata": {"source": hc["source"], "header": hc["header"]},
                }
            )

    return final_chunks
