from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from rag.ingestion import ingest_pdf
from rag.graph import run_crag

router = APIRouter()

# ===== REQUEST MODELS =====
class QuestionRequest(BaseModel):
    question: str

# ===== ENDPOINTS =====

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and ingest it into ChromaDB.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_bytes = await file.read()
    result = ingest_pdf(file_bytes, file.filename)
    return result


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Ask a question and get answer with citations via CRAG pipeline.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    result = run_crag(request.question)
    return result