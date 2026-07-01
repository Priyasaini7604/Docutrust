from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import tempfile
import os

# Embedding model — free, no API key needed
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

CHROMA_PATH = "./chroma_db"

def ingest_pdf(file_bytes: bytes, filename: str) -> dict:
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        client.delete_collection("docutrust")
    except:
        pass
    # Step 1: PDF ko temp file mein save karo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        # Step 2: PDF load karo
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

        # Step 3: Chunks mein todo
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=350,
            chunk_overlap=80,
        )
        chunks = splitter.split_documents(pages)

        # Step 4: ChromaDB mein store karo
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
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
        embedding_function=embeddings,
        collection_name="docutrust",
    )