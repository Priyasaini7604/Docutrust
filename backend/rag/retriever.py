from rag.ingestion import get_vectorstore

def retrieve_chunks(query: str, k: int = 4) -> list:
    """
    Retrieve relevant chunks from ChromaDB based on user query
    k = number of chunks to retrieve (default 4)
    """
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    docs = retriever.invoke(query)
    return docs