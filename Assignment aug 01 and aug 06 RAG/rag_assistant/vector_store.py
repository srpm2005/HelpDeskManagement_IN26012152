import json
import math
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    """
    Hybrid Vector Store and Keyword Matcher for RAG Knowledge Assistant.
    Combines TF-IDF n-gram vector embeddings with domain-specific keyword boosting.
    """
    
    def __init__(self, db_path: str = "vector_db.json"):
        self.db_path = Path(db_path)
        self.chunks: List[Dict[str, Any]] = []
        self.vectorizer: TfidfVectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            sublinear_tf=True,
            stop_words="english"
        )
        self.tfidf_matrix = None
        self.is_indexed = False

    def build_index(self, chunks: List[Dict[str, Any]]) -> None:
        """Build vector index from list of document chunks."""
        self.chunks = chunks
        if not chunks:
            print("[VectorStore] No chunks provided to index.")
            return

        corpus = []
        for chunk in chunks:
            # Combine title, section, source file, and content for rich feature representation
            text_repr = f"{chunk.get('title', '')} {chunk.get('section', '')} {chunk.get('source_file', '')} {chunk.get('content', '')}"
            corpus.append(text_repr)

        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        self.is_indexed = True
        print(f"[VectorStore] Successfully indexed {len(chunks)} chunks into vector space.")
        self.save_index()

    def search(self, query: str, top_k: int = 4) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search vector database for top_k most relevant chunks matching the query.
        Returns list of (chunk_dict, score) tuples sorted by relevance.
        """
        if not self.is_indexed or self.tfidf_matrix is None:
            if self.db_path.exists():
                self.load_index()
            else:
                raise ValueError("Vector store index is not built. Call build_index() first.")

        query_vec = self.vectorizer.transform([query])
        cosine_sims = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        query_terms = set(query.lower().replace("/", " ").replace(".", " ").split())
        scored_chunks = []

        for idx, base_score in enumerate(cosine_sims):
            chunk = self.chunks[idx]
            content_lower = chunk.get("content", "").lower()
            title_lower = chunk.get("title", "").lower()
            source_lower = chunk.get("source_file", "").lower()
            
            # Boost score if specific domain terms match in title, source_file, or content
            keyword_boost = 0.0
            for term in query_terms:
                if len(term) > 2:
                    if term in source_lower:
                        keyword_boost += 0.20
                    if term in title_lower:
                        keyword_boost += 0.15
                    if term in content_lower:
                        keyword_boost += 0.05
                        
            final_score = float(base_score) + keyword_boost
            scored_chunks.append((chunk, final_score))

        # Sort by relevance score descending
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        return scored_chunks[:top_k]

    def save_index(self) -> None:
        """Persist chunks to JSON database file."""
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, indent=2)
        print(f"[VectorStore] Persisted database to {self.db_path}")

    def load_index(self) -> None:
        """Load database from JSON file and rebuild TF-IDF matrix."""
        if not self.db_path.exists():
            raise FileNotFoundError(f"Vector DB file {self.db_path} not found.")

        with open(self.db_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        corpus = [
            f"{c.get('title', '')} {c.get('section', '')} {c.get('source_file', '')} {c.get('content', '')}"
            for c in self.chunks
        ]
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        self.is_indexed = True
        print(f"[VectorStore] Loaded {len(self.chunks)} chunks from {self.db_path}.")
