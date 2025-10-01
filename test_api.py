#!/usr/bin/env python3
"""
Simple test script to verify the API is working
"""

import subprocess
import sys
import os

# Activate virtual environment and run the test
def run_with_venv():
    venv_python = os.path.join(os.path.dirname(__file__), 'venv', 'bin', 'python')
    if os.path.exists(venv_python):
        subprocess.run([venv_python, __file__])
        return
    else:
        print("Virtual environment not found. Please run ./setup.sh first.")
        sys.exit(1)

if __name__ == "__main__":
    # Check if we're already in the virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # We're in a virtual environment, run the test
        import requests
        import json
        import time
    else:
        # Not in virtual environment, activate it and run
        run_with_venv()
        sys.exit(0)

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Website Content Search API")
    print("=" * 40)
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        print("Make sure the backend is running: ./start_backend.sh")
        return False
    
    # Test search endpoint
    print("\n2. Testing search endpoint...")
    test_data = {
        "url": "https://httpbin.org/html",
        "query": "test content"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/search",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search successful!")
            print(f"   Found {len(data.get('results', []))} results")
            print(f"   Total chunks: {data.get('total_chunks', 0)}")
            return True
        else:
            print(f"❌ Search failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Search request failed: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    if success:
        print("\n🎉 API test completed successfully!")
    else:
        print("\n💥 API test failed!")
        exit(1)
