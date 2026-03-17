#!/usr/bin/env python3
"""
Endee RAG Assistant Setup Script
This script helps you set up the Endee server and verify everything is working.
"""
import subprocess
import requests
import sys
import time
from pathlib import Path

def check_docker():
    """Check if Docker is installed and running"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        print(f"✅ Docker found: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ Docker is not installed!")
        print("\n📋 Please install Docker Desktop first:")
        print("1. Download from: https://www.docker.com/products/docker-desktop/")
        print("2. Install and start Docker Desktop")
        print("3. Run this script again")
        return False

def check_port_8080():
    """Check if port 8080 is already in use"""
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        if ':8080' in result.stdout:
            print("⚠️  Port 8080 is already in use!")
            
            # Try to find what's using it
            lines = [line for line in result.stdout.split('\n') if ':8080' in line]
            if lines:
                print(f"Details: {lines[0].strip()}")
            
            print("\n🔧 Options:")
            print("1. Stop the service using port 8080")
            print("2. Use a different port (update ENDEE_URL in config.py to http://127.0.0.1:8081)")
            print("3. Run Endee on port 8081:")
            print("   docker run --ulimit nofile=100000:100000 -p 8081:8080 -v ./endee-data:/data --name endee-server --restart unless-stopped endeeio/endee-server:latest")
            return False
        else:
            print("✅ Port 8080 is available")
            return True
    except Exception as e:
        print(f"⚠️  Could not check port 8080: {e}")
        return True

def start_endee_server():
    """Start the Endee server using Docker"""
    print("\n🐳 Starting Endee server...")
    
    # Create data directory
    data_dir = Path("./endee-data")
    data_dir.mkdir(exist_ok=True)
    
    cmd = [
        'docker', 'run',
        '--ulimit', 'nofile=100000:100000',
        '-p', '8080:8080',
        '-v', f'{data_dir.absolute()}:/data',
        '--name', 'endee-server',
        '--restart', 'unless-stopped',
        'endeeio/endee-server:latest'
    ]
    
    try:
        print("Running command:")
        print(' '.join(cmd))
        print("\nThis will take a few moments to download and start...")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Endee server started successfully!")
            return True
        else:
            print(f"❌ Failed to start Endee server: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⏰ Docker command timed out, but server might still be starting...")
        return True
    except Exception as e:
        print(f"❌ Error starting Endee server: {e}")
        return False

def wait_for_endee(max_wait=60):
    """Wait for Endee server to be ready"""
    print(f"\n⏳ Waiting for Endee server to be ready (max {max_wait} seconds)...")
    
    for i in range(max_wait):
        try:
            response = requests.get('http://localhost:8080/api/v1/health', timeout=2)
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

def test_endee_connection():
    """Test the Endee connection with our Python code"""
    print("\n🧪 Testing Endee connection with Python client...")
    
    try:
        # Import our modules
        sys.path.append('.')
        from ingest import check_endee_server
        
        if check_endee_server():
            print("✅ Python client can connect to Endee!")
            return True
        else:
            print("❌ Python client cannot connect to Endee")
            return False
    except Exception as e:
        print(f"❌ Error testing Python connection: {e}")
        return False

def main():
    """Main setup process"""
    print("🚀 Endee RAG Assistant Setup")
    print("=" * 50)
    
    # Step 1: Check Docker
    if not check_docker():
        return False
    
    # Step 2: Check port availability
    if not check_port_8080():
        print("\n❌ Please resolve the port conflict before continuing.")
        return False
    
    # Step 3: Check if Endee is already running
    print("\n🔍 Checking if Endee server is already running...")
    try:
        response = requests.get('http://localhost:8080/api/v1/health', timeout=3)
        if response.status_code == 200:
            print("✅ Endee server is already running!")
            return test_endee_connection()
    except requests.exceptions.RequestException:
        print("❌ Endee server is not running")
    
    # Step 4: Start Endee server
    if not start_endee_server():
        return False
    
    # Step 5: Wait for Endee to be ready
    if not wait_for_endee():
        return False
    
    # Step 6: Test Python connection
    return test_endee_connection()

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run your Streamlit app: python app.py")
        print("2. Or run the backend: python backend_simple.py")
        print("3. Open http://localhost:8501 (Streamlit) or http://localhost:8000 (Backend API)")
        print("\n📚 For API docs: http://localhost:8000/docs")
    else:
        print("\n❌ Setup failed. Please check the errors above and try again.")
        print("\n🆘 For manual setup:")
        print("1. Install Docker Desktop")
        print("2. Run: docker run --ulimit nofile=100000:100000 -p 8080:8080 -v ./endee-data:/data --name endee-server --restart unless-stopped endeeio/endee-server:latest")
        print("3. Wait 30-60 seconds for server to start")
        print("4. Verify: curl http://localhost:8080/api/v1/health")
    
    sys.exit(0 if success else 1)
