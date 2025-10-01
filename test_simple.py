#!/usr/bin/env python3
"""
Simple test script to verify the API is working
"""

import subprocess
import sys
import os

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Website Content Search API")
    print("=" * 40)
    
    # Test health endpoint using curl
    print("1. Testing health endpoint...")
    try:
        result = subprocess.run(['curl', '-s', f"{base_url}/health"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("Make sure the backend is running: ./start_backend.sh")
        return False
    
    # Test search endpoint using curl
    print("\n2. Testing search endpoint...")
    test_data = '{"url": "https://httpbin.org/html", "query": "test content"}'
    
    try:
        result = subprocess.run([
            'curl', '-s', '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-d', test_data,
            f"{base_url}/api/search"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ Search successful!")
            print(f"   Response: {result.stdout[:200]}...")
            return True
        else:
            print(f"❌ Search failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Search request failed: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    if success:
        print("\n🎉 API test completed successfully!")
    else:
        print("\n💥 API test failed!")
        exit(1)
