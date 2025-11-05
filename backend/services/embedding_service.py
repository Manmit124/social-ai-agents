"""
Embedding Service - Generate and manage text embeddings using Gemini API.

This service uses Google's Gemini Embedding model to convert text into 
high-dimensional vectors for semantic search and similarity comparison.

Features:
- Generate embeddings for single or multiple texts
- Batch processing for efficiency
- Task-specific embeddings (document storage vs query search)
- Cosine similarity calculation
- Normalized embeddings for accurate comparisons
"""

import os
from typing import List, Dict, Optional
from google import genai
from google.genai import types
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingService:
    """Service for generating and managing text embeddings using Gemini API."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini Embedding service.
        
        Args:
            api_key: Optional Gemini API key. If not provided, uses GEMINI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Initialize Gemini client
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-embedding-001"
        
        # Use 768 dimensions (recommended, good quality, smaller size)
        # Can be changed to 1536 or 3072 for better quality
        self.dimension = 768
        
        print(f"✅ EmbeddingService initialized with model: {self.model} ({self.dimension}D)")
    
    def generate_embedding(
        self, 
        text: str, 
        task_type: str = "RETRIEVAL_DOCUMENT"
    ) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: The text to embed (max 2,048 tokens)
            task_type: Type of task - "RETRIEVAL_DOCUMENT" (for storing) 
                      or "RETRIEVAL_QUERY" (for searching)
        
        Returns:
            List of floats representing the embedding vector (normalized)
        
        Example:
            >>> service = EmbeddingService()
            >>> embedding = service.generate_embedding("Added ML prediction endpoint")
            >>> len(embedding)
            768
        """
        try:
            # Validate input
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")
            
            # Generate embedding
            result = self.client.models.embed_content(
                model=self.model,
                contents=text,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=self.dimension
                )
            )
            
            # Extract and normalize embedding
            embedding_values = result.embeddings[0].values
            normalized = self._normalize_embedding(embedding_values)
            
            return normalized
        
        except Exception as e:
            print(f"❌ Error generating embedding: {str(e)}")
            raise Exception(f"Failed to generate embedding: {str(e)}")
    
    def generate_embeddings_batch(
        self, 
        texts: List[str], 
        task_type: str = "RETRIEVAL_DOCUMENT"
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in one API call (more efficient).
        
        This is 80% more efficient than calling generate_embedding() multiple times.
        Recommended for processing GitHub commits, tweets, or any bulk data.
        
        Args:
            texts: List of texts to embed (each max 2,048 tokens)
            task_type: Type of task - "RETRIEVAL_DOCUMENT" or "RETRIEVAL_QUERY"
        
        Returns:
            List of embedding vectors (each normalized)
        
        Example:
            >>> service = EmbeddingService()
            >>> texts = ["Commit 1", "Commit 2", "Commit 3"]
            >>> embeddings = service.generate_embeddings_batch(texts)
            >>> len(embeddings)
            3
        """
        try:
            # Validate input
            if not texts or len(texts) == 0:
                raise ValueError("Texts list cannot be empty")
            
            # Filter out empty texts
            valid_texts = [t for t in texts if t and t.strip()]
            if len(valid_texts) == 0:
                raise ValueError("All texts are empty")
            
            # Generate embeddings in batch
            result = self.client.models.embed_content(
                model=self.model,
                contents=valid_texts,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=self.dimension
                )
            )
            
            # Extract and normalize all embeddings
            embeddings = [
                self._normalize_embedding(e.values) 
                for e in result.embeddings
            ]
            
            print(f"✅ Generated {len(embeddings)} embeddings in batch")
            return embeddings
        
        except Exception as e:
            print(f"❌ Error generating batch embeddings: {str(e)}")
            raise Exception(f"Failed to generate batch embeddings: {str(e)}")
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding specifically for search queries.
        
        Use this when you want to search for similar documents.
        Use generate_embedding() with RETRIEVAL_DOCUMENT for storing documents.
        
        Args:
            query: The search query text
        
        Returns:
            Normalized embedding vector optimized for search
        
        Example:
            >>> service = EmbeddingService()
            >>> query_emb = service.generate_query_embedding("machine learning projects")
            >>> # Compare with stored document embeddings
        """
        return self.generate_embedding(query, task_type="RETRIEVAL_QUERY")
    
    def calculate_similarity(
        self, 
        embedding1: List[float], 
        embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Cosine similarity ranges from -1 to 1:
        - 1.0: Identical meaning
        - 0.8-0.99: Very similar
        - 0.6-0.79: Somewhat similar
        - 0.4-0.59: Slightly similar
        - < 0.4: Not similar
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
        
        Returns:
            Similarity score between -1 and 1
        
        Example:
            >>> service = EmbeddingService()
            >>> emb1 = service.generate_embedding("Added API endpoint")
            >>> emb2 = service.generate_embedding("Created REST API")
            >>> similarity = service.calculate_similarity(emb1, emb2)
            >>> print(f"Similarity: {similarity:.2f}")
            Similarity: 0.87
        """
        try:
            # Convert to numpy arrays
            e1 = np.array(embedding1).reshape(1, -1)
            e2 = np.array(embedding2).reshape(1, -1)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(e1, e2)[0][0]
            
            return float(similarity)
        
        except Exception as e:
            print(f"❌ Error calculating similarity: {str(e)}")
            raise Exception(f"Failed to calculate similarity: {str(e)}")
    
    def find_most_similar(
        self, 
        query_embedding: List[float], 
        document_embeddings: List[Dict[str, any]],
        top_k: int = 5
    ) -> List[Dict[str, any]]:
        """
        Find the most similar documents to a query.
        
        Args:
            query_embedding: The query embedding vector
            document_embeddings: List of dicts with 'embedding' and other metadata
            top_k: Number of top results to return
        
        Returns:
            List of documents sorted by similarity (highest first)
        
        Example:
            >>> service = EmbeddingService()
            >>> query_emb = service.generate_query_embedding("machine learning")
            >>> docs = [
            ...     {"id": 1, "text": "ML project", "embedding": [...]},
            ...     {"id": 2, "text": "Web app", "embedding": [...]}
            ... ]
            >>> results = service.find_most_similar(query_emb, docs, top_k=2)
        """
        try:
            # Calculate similarity for each document
            results = []
            for doc in document_embeddings:
                if 'embedding' not in doc:
                    continue
                
                similarity = self.calculate_similarity(
                    query_embedding, 
                    doc['embedding']
                )
                
                # Add similarity score to document
                result = doc.copy()
                result['similarity'] = similarity
                results.append(result)
            
            # Sort by similarity (highest first)
            results.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Return top K results
            return results[:top_k]
        
        except Exception as e:
            print(f"❌ Error finding similar documents: {str(e)}")
            raise Exception(f"Failed to find similar documents: {str(e)}")
    
    def _normalize_embedding(self, values: List[float]) -> List[float]:
        """
        Normalize embedding vector to unit length.
        
        Required for 768 and 1536 dimensions to ensure accurate similarity.
        The 3072 dimension embeddings are already normalized by Gemini.
        
        Args:
            values: Raw embedding values
        
        Returns:
            Normalized embedding values (unit vector)
        """
        embedding_np = np.array(values)
        norm = np.linalg.norm(embedding_np)
        
        if norm > 0:
            normalized = embedding_np / norm
            return normalized.tolist()
        
        return values
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension size of embeddings generated by this service."""
        return self.dimension
    
    def get_model_info(self) -> Dict[str, any]:
        """
        Get information about the embedding model.
        
        Returns:
            Dictionary with model details
        """
        return {
            "model": self.model,
            "dimension": self.dimension,
            "max_input_tokens": 2048,
            "supported_task_types": [
                "RETRIEVAL_DOCUMENT",
                "RETRIEVAL_QUERY",
                "SEMANTIC_SIMILARITY",
                "CLASSIFICATION",
                "CLUSTERING"
            ],
            "provider": "Google Gemini API"
        }


# Singleton instance for reuse
_embedding_service = None

def get_embedding_service() -> EmbeddingService:
    """
    Get or create the singleton EmbeddingService instance.
    
    Returns:
        Shared EmbeddingService instance
    """
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service

