import base64
import tempfile
import os
import uuid

import shutil
from fastapi import UploadFile

def save_upload_file(upload_file: UploadFile) -> str:
    """
    Saves an uploaded file to a temporary location.
    Returns the path to the temporary file.
    """
    try:
        # distinct temporary file name
        suffix = os.path.splitext(upload_file.filename)[1]
        if not suffix:
             suffix = ".tmp"

        temp_filename = f"temp_audio_{uuid.uuid4()}{suffix}"
        temp_path = os.path.join(tempfile.gettempdir(), temp_filename)
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            
        return temp_path
    except Exception as e:
        raise ValueError(f"Failed to save uploaded file: {str(e)}")

def cleanup_file(path: str):
    """Removes the temporary file."""
    if os.path.exists(path):
        os.remove(path)
