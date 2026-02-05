from fastapi import FastAPI, Depends, File, UploadFile, Form
from fastapi.responses import JSONResponse, RedirectResponse
from .models import VoiceAnalysisResponse
from .auth import get_api_key
from .utils import save_upload_file, cleanup_file
from .classifier import classifier
import traceback
import os
from typing import Optional

app = FastAPI(title="AI Voice Detection API", version="1.0")

@app.get("/")
async def root():
    return {"status": "success", "message": "AI Voice Detection API is online. Visit /docs for documentation."}

@app.post("/api/voice-detection", response_model=VoiceAnalysisResponse)
async def detect_voice(
    file: UploadFile = File(...),
    language: Optional[str] = Form("English"),
    api_key: str = Depends(get_api_key)
):
    temp_path = None
    try:
        # 1. Save Uploaded File
        try:
            temp_path = save_upload_file(file)
        except ValueError as ve:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": str(ve)}
            )

        # 2. Predict
        try:
            label, confidence, explanation = classifier.predict_voice(temp_path)
        except Exception as e:
            print(f"Prediction Error: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Internal processing error during analysis"}
            )

        if label is None:
             return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Model not initialized properly"}
            )
        
        # 3. Construct Response
        return VoiceAnalysisResponse(
            status="success",
            language=language,
            classification=label,
            confidenceScore=round(confidence, 2),
            explanation=explanation
        )

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Unexpected error: {str(e)}"}
        )
        
    finally:
        # 4. Cleanup
        if temp_path:
            cleanup_file(temp_path)

@app.get("/health")
def health_check():
    return {"status": "running", "message": "AI Voice Detection API is active"}
