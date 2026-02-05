from typing import List, Dict
from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore
from app.models import Document


class Retriever:
    
    def __init__(self, vector_store: VectorStore, embedding_model: EmbeddingModel):
       
        self.vector_store = vector_store
        self.embedding_model = embedding_model
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Document]:

        query_embedding = self.embedding_model.embed_text(query)
        
        results = self.vector_store.search(query_embedding, top_k=top_k)
    
        documents = []
        
        if results['documents'] and len(results['documents']) > 0:
            docs = results['documents'][0]  
            distances = results['distances'][0] if 'distances' in results else [0] * len(docs)
            
            for doc_content, distance in zip(docs, distances):
                import math
                score = math.exp(-distance)
                
                documents.append(
                    Document(
                        content=doc_content,
                        score=round(score, 4)
                    )
                )
        
        return documents
    
    def get_stats(self) -> Dict:
        return self.vector_store.get_collection_stats()
