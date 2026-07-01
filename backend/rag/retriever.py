from rag.ingestion import get_vectorstore

def retrieve_chunks(query: str, k: int = 8) -> list:
    """
    Retrieve relevant chunks using similarity search.
    Uses higher k value to cast a wider net, letting the grader
    filter down to truly relevant chunks.
    """
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "fetch_k": k * 3, "lambda_mult": 0.5}
    )
    docs = retriever.invoke(query)
    return docs