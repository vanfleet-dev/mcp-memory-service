#!/usr/bin/env python3
"""
Complete test suite for the HTTP/SSE + SQLite-vec implementation.
Runs all tests in sequence to validate the entire system.
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def check_server_health():
    """Check if the server is running and healthy."""
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_test_script(script_name, description):
    """Run a test script and return success status."""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print('='*60)
    
    try:
        # Run the test script
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent / script_name)
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Test PASSED")
            if result.stdout:
                print("Output:", result.stdout[-500:])  # Last 500 chars
            return True
        else:
            print("❌ Test FAILED")
            print("Error:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Test TIMED OUT")
        return False
    except Exception as e:
        print(f"❌ Test ERROR: {e}")
        return False

def main():
    """Run the complete test suite."""
    print("🚀 MCP Memory Service - Complete Test Suite")
    print("=" * 60)
    
    # Check if server is running
    if not check_server_health():
        print("❌ Server is not running or not healthy!")
        print("💡 Please start the server first:")
        print("   python scripts/run_http_server.py")
        return 1
    
    print("✅ Server is healthy and ready for testing")
    
    # Test suite configuration
    tests = [
        ("test_memory_simple.py", "Memory CRUD Operations Test"),
        ("test_search_api.py", "Search API Functionality Test"),
        ("test_sse_events.py", "Real-time SSE Events Test"),
    ]
    
    results = []
    
    # Run each test
    for script, description in tests:
        success = run_test_script(script, description)
        results.append((description, success))
        
        if success:
            print(f"✅ {description} - PASSED")
        else:
            print(f"❌ {description} - FAILED")
        
        # Brief pause between tests
        time.sleep(2)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print('='*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {description}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is working perfectly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} tests failed. Check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())