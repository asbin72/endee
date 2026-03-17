#!/usr/bin/env python3
"""
Test script to verify different documents return different results
"""
from ingest import ingest_document
from rag import run_rag

def test_different_documents():
    print("🧪 Testing Different Documents with Different Queries")
    print("=" * 60)
    
    # Test with AI-related document
    print("\n📄 Ingesting AI Document...")
    result1 = ingest_document('ai_doc.txt', 'This document discusses artificial intelligence, machine learning algorithms, and neural networks for data processing.')
    print(f"✅ AI Document: {result1['inserted']} chunks inserted")
    
    # Test with non-AI document  
    print("\n📄 Ingesting Cooking Document...")
    result2 = ingest_document('cooking_doc.txt', 'This recipe explains how to bake chocolate cake with flour, sugar, eggs, and butter. Preheat oven to 350 degrees.')
    print(f"✅ Cooking Document: {result2['inserted']} chunks inserted")
    
    print("\n" + "=" * 60)
    print("🔍 Testing Queries")
    print("=" * 60)
    
    # Query about AI
    print("\n❓ Query: 'What is machine learning?'")
    answer1, results1 = run_rag('What is machine learning?')
    print(f"📊 Results: {len(results1)} chunks found")
    for i, r in enumerate(results1):
        similarity = r.get('similarity', 0)
        source = r.get('meta', {}).get('source', 'unknown')
        print(f"  {i+1}. Similarity: {similarity:.3f} - Source: {source}")
    
    print("\n" + "-" * 40)
    
    # Query about cooking
    print("\n❓ Query: 'How to bake a cake?'")
    answer2, results2 = run_rag('How to bake a cake?')
    print(f"📊 Results: {len(results2)} chunks found")
    for i, r in enumerate(results2):
        similarity = r.get('similarity', 0)
        source = r.get('meta', {}).get('source', 'unknown')
        print(f"  {i+1}. Similarity: {similarity:.3f} - Source: {source}")
    
    print("\n" + "=" * 60)
    print("📈 Analysis:")
    print("=" * 60)
    
    # Analyze results
    ai_top_source = results1[0].get('meta', {}).get('source', 'unknown') if results1 else 'none'
    cooking_top_source = results2[0].get('meta', {}).get('source', 'unknown') if results2 else 'none'
    
    if ai_top_source == 'ai_doc.txt':
        print("✅ AI query correctly returned AI document first")
    else:
        print("❌ AI query did not return AI document first")
    
    if cooking_top_source == 'cooking_doc.txt':
        print("✅ Cooking query correctly returned cooking document first")
    else:
        print("❌ Cooking query did not return cooking document first")
    
    print(f"\n🎯 AI Query Top Source: {ai_top_source}")
    print(f"🎯 Cooking Query Top Source: {cooking_top_source}")
    
    print("\n🎉 Test Complete!")

if __name__ == "__main__":
    test_different_documents()
