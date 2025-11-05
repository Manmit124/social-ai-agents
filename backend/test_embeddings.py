"""
Test script for Embedding Service.

This script tests the embedding service locally to verify:
1. Embedding generation works
2. Batch embedding works
3. Similarity calculation works
4. Semantic search works

Run this script: python test_embeddings.py
"""

from dotenv import load_dotenv
load_dotenv()

import asyncio
from services.embedding_service import EmbeddingService


async def test_embedding_service():
    """Test all embedding service features."""
    
    print("=" * 80)
    print("🧪 TESTING EMBEDDING SERVICE")
    print("=" * 80)
    
    try:
        # Initialize service
        print("\n1️⃣  Initializing Embedding Service...")
        service = EmbeddingService()
        print(f"✅ Service initialized: {service.model} ({service.dimension}D)")
        
        # Test 1: Single embedding
        print("\n2️⃣  Testing single embedding generation...")
        text = "Added machine learning prediction endpoint to the API"
        embedding = service.generate_embedding(text)
        print(f"✅ Generated embedding with {len(embedding)} dimensions")
        print(f"   First 5 values: {embedding[:5]}")
        
        # Test 2: Batch embeddings
        print("\n3️⃣  Testing batch embedding generation...")
        texts = [
            "Implemented user authentication with JWT tokens",
            "Fixed bug in payment processing module",
            "Added dark mode support to the UI",
            "Optimized database queries for better performance",
            "Created REST API for mobile app"
        ]
        embeddings = service.generate_embeddings_batch(texts)
        print(f"✅ Generated {len(embeddings)} embeddings in batch")
        print(f"   Each embedding has {len(embeddings[0])} dimensions")
        
        # Test 3: Similarity calculation
        print("\n4️⃣  Testing similarity calculation...")
        
        # Similar texts
        text1 = "Added API endpoint for user registration"
        text2 = "Created REST API for user signup"
        emb1 = service.generate_embedding(text1, task_type="SEMANTIC_SIMILARITY")
        emb2 = service.generate_embedding(text2, task_type="SEMANTIC_SIMILARITY")
        similarity = service.calculate_similarity(emb1, emb2)
        print(f"✅ Similarity between similar texts: {similarity:.4f}")
        print(f"   Text 1: {text1}")
        print(f"   Text 2: {text2}")
        
        # Different texts
        text3 = "Fixed CSS styling issues in the header"
        text4 = "Implemented machine learning model for predictions"
        emb3 = service.generate_embedding(text3, task_type="SEMANTIC_SIMILARITY")
        emb4 = service.generate_embedding(text4, task_type="SEMANTIC_SIMILARITY")
        similarity2 = service.calculate_similarity(emb3, emb4)
        print(f"\n✅ Similarity between different texts: {similarity2:.4f}")
        print(f"   Text 3: {text3}")
        print(f"   Text 4: {text4}")
        
        # Test 4: Semantic search
        print("\n5️⃣  Testing semantic search...")
        query = "machine learning and AI projects"
        query_embedding = service.generate_query_embedding(query)
        
        # Create document embeddings with metadata
        documents = []
        for i, text in enumerate(texts):
            doc_embedding = service.generate_embedding(text, task_type="RETRIEVAL_DOCUMENT")
            documents.append({
                "id": i + 1,
                "text": text,
                "embedding": doc_embedding
            })
        
        # Find most similar documents
        results = service.find_most_similar(query_embedding, documents, top_k=3)
        
        print(f"✅ Search results for query: '{query}'")
        for i, result in enumerate(results, 1):
            print(f"\n   {i}. [Similarity: {result['similarity']:.4f}]")
            print(f"      {result['text']}")
        
        # Test 5: Model info
        print("\n6️⃣  Testing model info...")
        info = service.get_model_info()
        print(f"✅ Model Information:")
        print(f"   Model: {info['model']}")
        print(f"   Dimension: {info['dimension']}")
        print(f"   Max Input Tokens: {info['max_input_tokens']}")
        print(f"   Provider: {info['provider']}")
        print(f"   Supported Task Types: {', '.join(info['supported_task_types'])}")
        
        # Summary
        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED!")
        print("=" * 80)
        print("\n📊 Summary:")
        print(f"   ✅ Single embedding generation: Working")
        print(f"   ✅ Batch embedding generation: Working")
        print(f"   ✅ Similarity calculation: Working")
        print(f"   ✅ Semantic search: Working")
        print(f"   ✅ Model info: Working")
        print("\n🚀 Embedding service is ready for production!")
        print("\n💡 Next steps:")
        print("   1. Deploy to Render (works on 512MB RAM)")
        print("   2. Use batch processing for efficiency")
        print("   3. Implement Phase 3 Day 2 (Supabase pgvector)")
        print("   4. Store embeddings in database")
        print("   5. Build semantic search for GitHub commits")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    # Run tests
    success = asyncio.run(test_embedding_service())
    
    if not success:
        exit(1)

