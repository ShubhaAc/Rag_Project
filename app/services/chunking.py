from langchain_text_splitters import RecursiveCharacterTextSplitter, TokenTextSplitter

def chunk_by_recursive(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(text)


def chunk_by_token(text: str) -> list[str]:
    splitter = TokenTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )
    return splitter.split_text(text)


def get_chunks(text: str, strategy: str) -> list[str]:
    if strategy == "recursive":
        return chunk_by_recursive(text)
    elif strategy == "token":
        return chunk_by_token(text)
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy}")