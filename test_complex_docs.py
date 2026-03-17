#!/usr/bin/env python3
"""
Test script to verify the similarity search works correctly with complex documents
"""
from ingest import ingest_document
from rag import run_rag

def test_complex_documents():
    print("🧪 Testing Complex Documents with Improved Similarity")
    print("=" * 65)
    
    # Test with AI-related document
    print("\n📄 Ingesting AI Document...")
    ai_doc = """This document discusses artificial intelligence, machine learning algorithms, 
    and neural networks for data processing. Modern AI systems use deep learning techniques 
    to analyze large datasets and make predictions."""
    result1 = ingest_document('ai_research.txt', ai_doc)
    print(f"✅ AI Document: {result1['inserted']} chunks inserted")
    
    # Test with cooking document
    print("\n📄 Ingesting Cooking Document...")
    cooking_doc = """This recipe explains how to bake chocolate cake with flour, sugar, eggs, and butter. 
    Preheat oven to 350 degrees. Mix ingredients thoroughly and bake for 30 minutes."""
    result2 = ingest_document('baking_recipe.txt', cooking_doc)
    print(f"✅ Cooking Document: {result2['inserted']} chunks inserted")
    
    # Test with resume/CV document (the problematic content)
    print("\n📄 Ingesting Resume Document...")
    resume_doc = """ll-stack application modules. –Implemented backend logic using Spring and Hibernate 
    with structured database integration. Certifications •CCNA Networking Certification– TEKSOL GLOBAL, 
    demonstrating strong fundamentals in networking concepts and protocols. Education DMI College of 
    Engineering 2022 – 2026 B.Tech in Information Technology, CGPA: 8.0 India Little Flower Matriculation 
    Higher Secondary School 2021 – 2022 SSLC, Percentage: 72.6% India Little Flower Matriculation 
    Higher Secondary School 2019 – 2020 HSC, Percentage: 68.8% India"""
    result3 = ingest_document('resume.txt', resume_doc)
    print(f"✅ Resume Document: {result3['inserted']} chunks inserted")
    
    print("\n" + "=" * 65)
    print("🔍 Testing Specific Queries")
    print("=" * 65)
    
    # Test queries
    queries = [
        ("What is machine learning?", "AI-related query"),
        ("How to bake a cake?", "Cooking-related query"),
        ("What are your certifications?", "Resume-related query"),
        ("Tell me about neural networks", "AI-specific query"),
        ("What ingredients do I need for baking?", "Cooking-specific query")
    ]
    
    for query, description in queries:
        print(f"\n❓ Query: '{query}' ({description})")
        answer, results = run_rag(query)
        print(f"📊 Results: {len(results)} chunks found")
        
        for i, r in enumerate(results[:3]):  # Show top 3
            similarity = r.get('similarity', 0)
            source = r.get('meta', {}).get('source', 'unknown')
            text_preview = r.get('meta', {}).get('text', '')[:100] + "..."
            print(f"  {i+1}. Similarity: {similarity:.3f} - Source: {source}")
            print(f"     Preview: {text_preview}")
        
        print("-" * 50)
    
    print("\n" + "=" * 65)
    print("📈 Analysis:")
    print("=" * 65)
    
    # Test specific scenarios
    print("\n🎯 Testing AI Query vs Different Documents:")
    ai_answer, ai_results = run_rag("What is machine learning?")
    ai_top = ai_results[0].get('meta', {}).get('source', 'none') if ai_results else 'none'
    print(f"AI Query Top Result: {ai_top}")
    
    print("\n🎯 Testing Cooking Query vs Different Documents:")
    cooking_answer, cooking_results = run_rag("How to bake a cake?")
    cooking_top = cooking_results[0].get('meta', {}).get('source', 'none') if cooking_results else 'none'
    print(f"Cooking Query Top Result: {cooking_top}")
    
    print("\n🎯 Testing Resume Query vs Different Documents:")
    resume_answer, resume_results = run_rag("What are your certifications?")
    resume_top = resume_results[0].get('meta', {}).get('source', 'none') if resume_results else 'none'
    print(f"Resume Query Top Result: {resume_top}")
    
    # Check if queries return appropriate documents
    correct_matches = 0
    if ai_top == 'ai_research.txt':
        correct_matches += 1
        print("✅ AI query correctly matched AI document")
    else:
        print("❌ AI query did not match AI document")
    
    if cooking_top == 'baking_recipe.txt':
        correct_matches += 1
        print("✅ Cooking query correctly matched cooking document")
    else:
        print("❌ Cooking query did not match cooking document")
    
    if resume_top == 'resume.txt':
        correct_matches += 1
        print("✅ Resume query correctly matched resume document")
    else:
        print("❌ Resume query did not match resume document")
    
    print(f"\n🏆 Overall Accuracy: {correct_matches}/3 queries matched correctly")
    
    if correct_matches >= 2:
        print("🎉 Similarity search is working well!")
    else:
        print("⚠️  Similarity search needs improvement")
    
    print("\n🎉 Test Complete!")

if __name__ == "__main__":
    test_complex_documents()
