# AI Voice Detection API

This project provides a FastAPI-based REST API for detecting AI-generated voices. Use this API to analyze audio files and determine if they are real or AI-generated.

## Prerequisites

- Python 3.8+
- pip

## Installation

1.  **Clone or navigate to the project directory:**
    ```bash
    cd "c:\Users\janan\OneDrive\Attachments\Hackathons\GUVI HCL\voice-detection-api"
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate  # Mac/Linux
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the API

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

- The API will differ to `http://127.0.0.1:8000`.
- **Interactive Documentation**: Visit `http://127.0.0.1:8000/docs` to see the Swagger UI and test endpoints directly in your browser.

## Testing

You can run the included test script to verify the API is responding:

```bash
python tests/test_api.py
```

*Note: The test script might report a 500 error if it uses a dummy invalid audio file, but it confirms the server is reachable.*

## Training the Model (Optional)

If you have a dataset and want to retrain the classifier:

1.  Place your dataset in a `driver_audio` folder (or update the script).
2.  Run the training script:
    ```bash
    python ml_tools/train_model.py
    ```
