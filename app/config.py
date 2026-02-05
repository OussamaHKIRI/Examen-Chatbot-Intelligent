from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    gemini_api_key: str = "AIzaSyBNTwuXFuuUKxnSE-sLgGT7SimJajBS5g0"
    
    embedding_model: str = "all-MiniLM-L6-v2"
    gemini_model: str = "gemini-1.5-flash"
    
    chroma_db_path: str = "./chroma_db"
    collection_name: str = "ecommerce_faq"
    
    dataset_path: str = "./data/Ecommerce_FAQ_Chatbot_dataset.csv"
    
    top_k: int = 5
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
