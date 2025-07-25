#!/usr/bin/env python3
"""Simple test for memory CRUD operations."""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_memory_crud():
    """Test the complete CRUD workflow for memories."""
    
    print("Testing Memory CRUD Operations")
    print("=" * 40)
    
    # Test 1: Health check
    print("\n[1] Health check...")
    try:
        resp = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if resp.status_code == 200:
            print("[PASS] Server is healthy")
        else:
            print(f"[FAIL] Health check failed: {resp.status_code}")
            return
    except Exception as e:
        print(f"[FAIL] Cannot connect: {e}")
        return
    
    # Test 2: Store memory
    print("\n[2] Storing memory...")
    test_memory = {
        "content": "Test memory for API verification",
        "tags": ["test", "api"],
        "memory_type": "test",
        "metadata": {"timestamp": time.time()}
    }
    
    try:
        resp = requests.post(
            f"{BASE_URL}/api/memories",
            json=test_memory,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if resp.status_code == 200:
            result = resp.json()
            if result["success"]:
                content_hash = result["content_hash"]
                print(f"[PASS] Memory stored: {content_hash[:12]}...")
            else:
                print(f"[FAIL] Storage failed: {result['message']}")
                return
        else:
            print(f"[FAIL] Storage failed: {resp.status_code}")
            print(f"Error: {resp.text}")
            return
    except Exception as e:
        print(f"[FAIL] Storage error: {e}")
        return
    
    # Test 3: List memories
    print("\n[3] Listing memories...")
    try:
        resp = requests.get(f"{BASE_URL}/api/memories?page=1&page_size=5", timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            print(f"[PASS] Found {len(result['memories'])} memories")
            print(f"Total: {result['total']}")
        else:
            print(f"[FAIL] Listing failed: {resp.status_code}")
    except Exception as e:
        print(f"[FAIL] Listing error: {e}")
    
    # Test 4: Delete memory
    print("\n[4] Deleting memory...")
    try:
        resp = requests.delete(f"{BASE_URL}/api/memories/{content_hash}", timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            if result["success"]:
                print("[PASS] Memory deleted")
            else:
                print(f"[FAIL] Deletion failed: {result['message']}")
        else:
            print(f"[FAIL] Deletion failed: {resp.status_code}")
    except Exception as e:
        print(f"[FAIL] Deletion error: {e}")
    
    print("\n" + "=" * 40)
    print("CRUD testing completed!")

if __name__ == "__main__":
    test_memory_crud()