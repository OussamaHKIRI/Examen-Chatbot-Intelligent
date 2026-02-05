import chromadb
from chromadb.config import Settings
from typing import List, Dict
import os


class VectorStore:
    
    def __init__(self, persist_directory: str, collection_name: str):
      
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        os.makedirs(persist_directory, exist_ok=True)
        
        print(f"Initializing ChromaDB at: {persist_directory}")
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f" Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "E-commerce FAQ chatbot knowledge base"}
            )
            print(f" Created new collection: {collection_name}")
    
    def populate(self, documents: List[Dict[str, any]], embeddings: List[List[float]]):
       
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings")
        
        existing_count = self.collection.count()
        if existing_count > 0:
            print(f"Collection already contains {existing_count} documents. Skipping population.")
            return
        
        print(f"Populating vector store with {len(documents)} documents...")
        
        ids = [doc['id'] for doc in documents]
        contents = [doc['content'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            end_idx = min(i + batch_size, len(documents))
            
            self.collection.add(
                ids=ids[i:end_idx],
                documents=contents[i:end_idx],
                embeddings=embeddings[i:end_idx],
                metadatas=metadatas[i:end_idx]
            )
            
            print(f"  Added batch {i//batch_size + 1}: {end_idx}/{len(documents)} documents")
        

    def search(self, query_embedding: List[float], top_k: int = 5) -> Dict:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return results
    
    def get_collection_stats(self) -> Dict:
    
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "document_count": count,
            "persist_directory": self.persist_directory
        }
    
    def reset_collection(self):
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "E-commerce FAQ chatbot knowledge base"}
        )
        print(f" Collection reset: {self.collection_name}")
