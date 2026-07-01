from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

# Initialize FastAPI app
app = FastAPI(
    title="DocuTrust API",
    description="Enterprise RAG Platform with Self-Correction",
    version="1.0.0"
)

# CORS middleware — allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")

# Health check endpoint
@app.get("/")
async def root():
    return {"status": "DocuTrust API is running!"}