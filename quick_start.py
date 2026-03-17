#!/usr/bin/env python3
"""
Quick Start Script for Endee RAG Assistant (No Docker Required)
This script helps you get started with either Docker Endee or Mock Endee
"""
import subprocess
import requests
import sys
import time
import threading
from pathlib import Path

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def start_mock_endee():
    """Start the mock Endee server"""
    print("🚀 Starting Mock Endee Server...")
    print("📝 This simulates Endee for testing without Docker")
    
    try:
        # Start mock server in background
        subprocess.run([sys.executable, 'mock_endee.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Mock Endee Server stopped")
    except Exception as e:
        print(f"❌ Error starting mock server: {e}")

def wait_for_endee(max_wait=30, url="http://localhost:8080/api/v1/health"):
    """Wait for Endee (real or mock) to be ready"""
    print(f"⏳ Waiting for Endee server to be ready...")
    
    for i in range(max_wait):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print("✅ Endee server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i % 5 == 0:
            print(f"  Checking... ({i+1}/{max_wait})")
        time.sleep(1)
    
    print("❌ Endee server did not become ready in time")
    return False

def test_application():
    """Test the RAG application"""
    print("\n🧪 Testing RAG Application...")
    
    try:
        # Test Python connection
        sys.path.append('.')
        from ingest import check_endee_server
        
        if check_endee_server():
            print("✅ Python client can connect to Endee!")
            return True
        else:
            print("❌ Python client cannot connect to Endee")
            return False
    except Exception as e:
        print(f"❌ Error testing application: {e}")
        return False

def main():
    """Main setup process"""
    print("🎯 Endee RAG Assistant Quick Start")
    print("=" * 50)
    
    # Check Docker availability
    docker_available = check_docker()
    
    if docker_available:
        print("✅ Docker is available")
        choice = input("\nChoose your Endee setup:\n1. Use Docker Endee (recommended)\n2. Use Mock Endee (for testing)\n3. Try Docker first, fallback to mock\n\nChoice (1-3): ").strip()
        
        if choice == "1":
            print("\n🐳 Setting up Docker Endee...")
            print("Please run: python setup_endee.py")
            return False
        elif choice == "2":
            print("\n🎭 Using Mock Endee...")
            start_mock_endee()
        elif choice == "3":
            print("\n🔄 Trying Docker first...")
            # Try to start Docker Endee
            try:
                result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Docker is running, checking for Endee container...")
                    # Check if Endee is already running
                    try:
                        response = requests.get('http://localhost:8080/api/v1/health', timeout=3)
                        if response.status_code == 200:
                            print("✅ Endee Docker container is already running!")
                            return test_application()
                    except:
                        print("❌ Endee container not found, please run: python setup_endee.py")
                        return False
                else:
                    print("❌ Docker is not running")
            except:
                print("❌ Docker not available")
            
            print("🔄 Falling back to Mock Endee...")
            start_mock_endee()
        else:
            print("❌ Invalid choice")
            return False
    else:
        print("❌ Docker not found, using Mock Endee...")
        start_mock_endee()
    
    return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🆘 For help:")
        print("1. Install Docker Desktop")
        print("2. Run: python setup_endee.py")
        print("3. Or use mock server: python mock_endee.py")
