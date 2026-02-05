import requests
import sys

API_URL = "http://127.0.0.1:8000/api/voice-detection"
API_KEY = "sk_test_123456789"

def test_api(file_path):
    print(f"Testing API with file: {file_path}")
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            headers = {"x-api-key": API_KEY}
            data = {"language": "English"}
            
            response = requests.post(API_URL, headers=headers, files=files, data=data)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("SUCCESS: API call worked.")
            else:
                print("FAILURE: API call failed.")
                
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_upload.py <path_to_audio_file>")
        # Default to a known file if exists for quick testing
        test_file = "data/human/Ambikapathy.mp3"
        test_api(test_file)
    else:
        test_api(sys.argv[1])
