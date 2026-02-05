from fastapi import APIRouter, HTTPException
from app.models import QueryRequest, SearchResponse, ChatbotResponse
from app.rag.retriever import Retriever
from app.rag.generator import Generator
from typing import Optional

router = APIRouter()

retriever: Optional[Retriever] = None
generator: Optional[Generator] = None


def set_retriever(ret: Retriever):
    global retriever
    retriever = ret


def set_generator(gen: Generator):
    global generator
    generator = gen


@router.post("/search", response_model=SearchResponse)
async def search_documents(request: QueryRequest):
    if retriever is None:
        raise HTTPException(
            status_code=500,
            detail="Retriever not initialized. Please ensure the system is properly configured."
        )
    
    try:
        documents = retriever.retrieve(request.query, top_k=5)
        return SearchResponse(
            query=request.query,
            top_documents=documents
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during document retrieval: {str(e)}"
        )


@router.post("/chat", response_model=ChatbotResponse)
async def chat(request: QueryRequest):
    if retriever is None or generator is None:
        raise HTTPException(
            status_code=500,
            detail="System not fully initialized. Please ensure all components are configured."
        )
    
    try:
        documents = retriever.retrieve(request.query, top_k=5)
        
        answer = generator.generate_answer(request.query, documents)
        
        return ChatbotResponse(
            query=request.query,
            top_documents=documents,
            response=answer
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during chat processing: {str(e)}"
        )


@router.get("/stats")
async def get_stats():
    if retriever is None:
        raise HTTPException(
            status_code=500,
            detail="Retriever not initialized"
        )
    
    try:
        stats = retriever.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving stats: {str(e)}"
        )
