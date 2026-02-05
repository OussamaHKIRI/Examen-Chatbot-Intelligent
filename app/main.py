from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.models import HealthResponse
from app.api import routes
from app.rag.data_loader import DataLoader
from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.rag.generator import Generator
from app import __version__


retriever = None
generator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    global retriever, generator

    try:
        embedding_model = EmbeddingModel(model_name=settings.embedding_model)
        
      
        vector_store = VectorStore(
            persist_directory=settings.chroma_db_path,
            collection_name=settings.collection_name
        )
        
        data_loader = DataLoader(dataset_path=settings.dataset_path)
        
        stats = vector_store.get_collection_stats()
        if stats['document_count'] == 0:
            
            documents = data_loader.load_faq_data()
            
            contents = [doc['content'] for doc in documents]
            embeddings = embedding_model.embed_batch(contents)
            
            vector_store.populate(documents, embeddings)
        else:
            print(f"Vector store already contains {stats['document_count']} documents. Skipping population.")
        
        retriever = Retriever(vector_store, embedding_model)
        routes.set_retriever(retriever)
        
        generator = Generator(
            api_key=settings.gemini_api_key,
            model_name=settings.gemini_model
        )
        routes.set_generator(generator)
        
       
        
    except Exception as e:
        print(f"\n Error during startup: {str(e)}")
        raise
    
    yield

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=HealthResponse)
async def health_check():
   
    return HealthResponse(
        version=__version__,
        swagger="/docs"
    )

app.include_router(routes.router, tags=["Chatbot"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
