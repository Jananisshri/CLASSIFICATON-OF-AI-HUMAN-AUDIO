"""
Test script to verify API authentication matches requirements document.
Tests three scenarios:
1. Valid API key - should return 200 OK
2. Invalid API key - should return 403 Forbidden
3. Missing API key - should return 401 Unauthorized
"""
import requests
import os

API_URL = "http://127.0.0.1:8000/api/voice-detection"
VALID_KEY = "sk_test_123456789"
INVALID_KEY = "wrong_key_12345"

# Use the test audio file
TEST_AUDIO = os.path.join(os.path.dirname(__file__), "..", "test_audio.wav")

def test_valid_api_key():
    """Test 1: Valid API key should work"""
    print("\n" + "="*60)
    print("TEST 1: Valid API Key (sk_test_123456789)")
    print("="*60)
    
    with open(TEST_AUDIO, "rb") as f:
        files = {"file": ("test.wav", f, "audio/wav")}
        headers = {"x-api-key": VALID_KEY}
        data = {"language": "English"}
        
        response = requests.post(API_URL, files=files, headers=headers, data=data)
        
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    if response.status_code == 200:
        print("✅ PASS: Valid API key accepted")
        return True
    else:
        print("❌ FAIL: Valid API key rejected")
        return False

def test_invalid_api_key():
    """Test 2: Invalid API key should return 403"""
    print("\n" + "="*60)
    print("TEST 2: Invalid API Key")
    print("="*60)
    
    with open(TEST_AUDIO, "rb") as f:
        files = {"file": ("test.wav", f, "audio/wav")}
        headers = {"x-api-key": INVALID_KEY}
        data = {"language": "English"}
        
        response = requests.post(API_URL, files=files, headers=headers, data=data)
        
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 403:
        print("✅ PASS: Invalid API key rejected with 403")
        return True
    else:
        print(f"❌ FAIL: Expected 403, got {response.status_code}")
        return False

def test_missing_api_key():
    """Test 3: Missing API key should return 401"""
    print("\n" + "="*60)
    print("TEST 3: Missing API Key")
    print("="*60)
    
    with open(TEST_AUDIO, "rb") as f:
        files = {"file": ("test.wav", f, "audio/wav")}
        # No x-api-key header
        data = {"language": "English"}
        
        response = requests.post(API_URL, files=files, data=data)
        
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 401:
        print("✅ PASS: Missing API key rejected with 401")
        return True
    else:
        print(f"❌ FAIL: Expected 401, got {response.status_code}")
        return False

if __name__ == "__main__":
    print("\n" + "🔐 API AUTHENTICATION REQUIREMENTS VERIFICATION" + "\n")
    print("Testing against requirements document:")
    print("- API must validate API key in 'x-api-key' header")
    print("- Requests without valid API key must be rejected")
    
    results = []
    
    try:
        results.append(test_valid_api_key())
        results.append(test_invalid_api_key())
        results.append(test_missing_api_key())
        
        print("\n" + "="*60)
        print("FINAL RESULTS")
        print("="*60)
        
        if all(results):
            print("✅ ALL TESTS PASSED - Implementation matches requirements!")
        else:
            print(f"❌ {results.count(False)} test(s) failed")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("Make sure the server is running: uvicorn app.main:app --reload")
