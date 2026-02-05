import json
from typing import List, Dict, Any
import os


class DataLoader:
    
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        
    def load_faq_data(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset not found at: {self.dataset_path}")
        try:
            with open(self.dataset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            questions_data = data.get('questions', [])
            
            if not questions_data:
                raise ValueError("No 'questions' array found in the JSON file")
            documents = []
            for idx, item in enumerate(questions_data):
                question = item.get('question', '').strip()
                answer = item.get('answer', '').strip()
                if not question or not answer:
                    continue
                formatted_doc = f"Question: {question}\nResponse: {answer}"
                
                documents.append({
                    'id': f"doc_{idx}",
                    'content': formatted_doc,
                    'metadata': {
                        'question': question,
                        'answer': answer,
                        'source': 'ecommerce_faq'
                    }
                })
            
            print(f" Loaded {len(documents)} FAQ documents from {self.dataset_path}")
            return documents
            
        except Exception as e:
            raise ValueError(f"Error loading dataset: {str(e)}")
    
    def get_sample_documents(self, n: int = 5) -> List[Dict[str, Any]]:
    
        all_docs = self.load_faq_data()
        return all_docs[:min(n, len(all_docs))]
