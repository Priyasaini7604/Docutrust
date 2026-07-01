from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import tempfile
import os

CHROMA_PATH = "./chroma_db"

# Lazy loading
_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        from langchain_community.embeddings import FastEmbedEmbeddings
        _embeddings = FastEmbedEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"  # lightest, ~50MB
        )
    return _embeddings


def ingest_pdf(file_bytes: bytes, filename: str) -> dict:
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        client.delete_collection("docutrust")
    except:
        pass

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=350,
            chunk_overlap=80,
        )
        chunks = splitter.split_documents(pages)

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=get_embeddings(),
            persist_directory=CHROMA_PATH,
            collection_name="docutrust",
        )

        return {
            "status": "success",
            "chunks": len(chunks),
            "pages": len(pages),
            "filename": filename,
        }

    finally:
        os.unlink(tmp_path)


def get_vectorstore():
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embeddings(),
        collection_name="docutrust",
    )