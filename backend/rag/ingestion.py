from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import tempfile
import os

CHROMA_PATH = "./chroma_db"

# Lazy loading — startup pe load nahi hoga
_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
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
            embedding=get_embeddings(),   # ← lazy call
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
        embedding_function=get_embeddings(),   # ← lazy call
        collection_name="docutrust",
    )