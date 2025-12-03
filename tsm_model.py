import os
import sys
import torch
import transformers

# Add contriever to sys.path to allow imports from src
sys.path.append(os.path.join(os.path.dirname(__file__), "contriever"))

from src.contriever import load_retriever

class TSMModel:
    def __init__(self, model_path="seungyoonee/tsm-contriever"):
        self.model_path = model_path
        print(f"Loading model from {model_path}...")
        self.model, self.tokenizer, _ = load_retriever(model_path)
        self.model.eval()

    def compute_score(self, query, document):
        with torch.no_grad():
            # Tokenize query
            query_inputs = self.tokenizer(
                [query], padding=True, truncation=True, return_tensors="pt"
            )
            
            # Tokenize document
            doc_inputs = self.tokenizer(
                [document], padding=True, truncation=True, return_tensors="pt"
            )

            # Compute embeddings
            
            query_emb = self.model(**query_inputs, normalize=True)
            doc_emb = self.model(**doc_inputs, normalize=True)

            # Compute dot product (which is cosine similarity since normalized)
            score = (query_emb @ doc_emb.T).item()
            
            return score
