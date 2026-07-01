import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

@asynccontextmanager
async def lifespan(app):
    async def keep_alive():
        import httpx
        while True:
            await asyncio.sleep(14 * 60)
            try:
                async with httpx.AsyncClient() as client:
                    await client.get("https://docutrust-backend-hdm4.onrender.com/")
            except:
                pass
    asyncio.create_task(keep_alive())
    yield

# Initialize FastAPI app
app = FastAPI(
    title="DocuTrust API",
    description="Enterprise RAG Platform with Self-Correction",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
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