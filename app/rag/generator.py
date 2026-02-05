import google.generativeai as genai
from typing import List
from app.models import Document


class Generator:
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
    
        self.model_name = model_name
        if not api_key:
            raise ValueError("Gemini API key is required. Please set GEMINI_API_KEY in .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        print(f"✓ Gemini model initialized: {model_name}")
    
    def generate_answer(self, query: str, documents: List[Document]) -> str:
        context = self._build_context(documents)
        prompt = self._create_rag_prompt(query, context)
        
        try:
            response = self.model.generate_content(prompt)
            answer = response.text.strip()
            return answer
        except Exception as e:
            return f"I apologize, but I encountered an error generating a response: {str(e)}"
    
    def _build_context(self, documents: List[Document]) -> str:
        context_parts = []
        for idx, doc in enumerate(documents, 1):
            context_parts.append(f"[Document {idx}]\n{doc.content}\n")
        
        return "\n".join(context_parts)
    
    def _create_rag_prompt(self, query: str, context: str) -> str:
        prompt = f"""You are a helpful e-commerce customer service assistant. Your task is to answer customer questions based ONLY on the provided context documents.

IMPORTANT RULES:
1. Answer ONLY based on the information in the context documents below
2. If the context doesn't contain relevant information to answer the question, say "I don't have enough information to answer that question based on our FAQ database."
3. Be concise, helpful, and professional
4. Do not make up information or use external knowledge
5. If multiple documents contain relevant information, synthesize them into a coherent answer

CONTEXT DOCUMENTS:
{context}

CUSTOMER QUESTION:
{query}

ANSWER:
"""
        return prompt
