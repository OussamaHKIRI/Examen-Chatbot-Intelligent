from pydantic import BaseModel, Field
from typing import List


class QueryRequest(BaseModel):
    """Request model for user queries."""
    query: str = Field(..., description="User's question", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What payment methods do you accept?"
            }
        }


class Document(BaseModel):
    """Model representing a retrieved document."""
    content: str = Field(..., description="Document content")
    score: float = Field(..., description="Relevance score", ge=0.0, le=1.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "Question: What payment methods do you accept?\nResponse: We accept credit cards, PayPal, and bank transfers.",
                "score": 0.95
            }
        }


class SearchResponse(BaseModel):
    """Response model for document search."""
    query: str = Field(..., description="Original query")
    top_documents: List[Document] = Field(..., description="Top K retrieved documents")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What payment methods do you accept?",
                "top_documents": [
                    {
                        "content": "Question: What payment methods do you accept?\nResponse: We accept credit cards, PayPal, and bank transfers.",
                        "score": 0.95
                    }
                ]
            }
        }


class ChatbotResponse(BaseModel):
    """Response model for the complete chatbot interaction."""
    query: str = Field(..., description="Original user query")
    top_documents: List[Document] = Field(..., description="Top K retrieved documents")
    response: str = Field(..., description="Generated answer from LLM")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What payment methods do you accept?",
                "top_documents": [
                    {
                        "content": "Question: What payment methods do you accept?\nResponse: We accept credit cards, PayPal, and bank transfers.",
                        "score": 0.95
                    }
                ],
                "response": "We accept multiple payment methods including credit cards, PayPal, and bank transfers for your convenience."
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    version: str = Field(..., description="API version")
    swagger: str = Field(..., description="Swagger documentation URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "version": "1.0.0",
                "swagger": "/docs"
            }
        }
