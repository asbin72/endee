#!/usr/bin/env python3
"""
Simple test client for Endee RAG Assistant Backend
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_upload():
    """Test the upload endpoint with a simple text file"""
    print("Testing upload endpoint...")
    
    # Create a simple test file content
    test_content = """This is a test document for the Endee RAG Assistant.
It contains some sample text that can be used for testing the RAG functionality.
The document discusses artificial intelligence and machine learning concepts.
AI is transforming many industries including healthcare, finance, and transportation.
Machine learning algorithms can process large amounts of data to find patterns."""
    
    files = {'files': ('test.txt', test_content, 'text/plain')}
    data = {'category': 'test'}
    
    response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_query():
    """Test the query endpoint"""
    print("Testing query endpoint...")
    
    query_data = {
        "query": "What is AI transforming?",
        "top_k": 3
    }
    
    response = requests.post(f"{BASE_URL}/query", json=query_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    print("=== Endee RAG Assistant Backend Test ===")
    print()
    
    try:
        test_health()
        
        print("Note: Upload test requires Endee to be properly configured.")
        print("If Endee is not connected, the upload will fail.")
        print()
        
        # Only test upload if Endee is connected
        health_response = requests.get(f"{BASE_URL}/health").json()
        if health_response.get('endee_connected'):
            test_upload()
            test_query()
        else:
            print("Skipping upload and query tests - Endee not connected")
            print("Please configure your ENDEE_AUTH_TOKEN in .env file")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to backend server")
        print("Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")
