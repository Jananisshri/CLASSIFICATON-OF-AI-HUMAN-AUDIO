import requests
import base64
import os
import sys

# CONFIGURATION
API_URL = "http://127.0.0.1:8000/api/voice-detection"
API_KEY = "sk_test_123456789"
FILE_PATH = "sample_audio.mp3" # <--- REPLACE THIS WITH YOUR MP3 FILE PATH

def test_audio_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        print("Please edit 'client.py' and set FILE_PATH to a valid MP3 file.")
        return

    print(f"Uploading {file_path}...")
    
    # Prepare file upload (multipart/form-data)
    with open(file_path, "rb") as f:
        files = {
            "file": (os.path.basename(file_path), f, "audio/mpeg")
        }
        
        data = {
            "language": "English"  # You can change this to Tamil, Hindi, etc.
        }
        
        headers = {
            "x-api-key": API_KEY
        }

        print("Sending request to API...")
        try:
            response = requests.post(API_URL, files=files, data=data, headers=headers)
            
            print("\n--- API RESPONSE ---")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ RESULT:")
                print(f"  Classification: {result.get('classification')}")
                print(f"  Confidence:     {result.get('confidenceScore')}")
                print(f"  Explanation:    {result.get('explanation')}")
                print(f"\n📄 Full JSON: {result}")
            else:
                print("❌ Error Response:")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Request Error: {e}")

if __name__ == "__main__":
    # Allow passing file path as argument: python client.py my_voice.mp3
    target_file = FILE_PATH
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        
    test_audio_file(target_file)
