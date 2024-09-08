from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import tempfile
import os
from TransformoDocs import TransformoDocs

app = FastAPI()
processor = TransformoDocs()

class FileResponse(BaseModel):
    text: List[str] = []
    images: List[Dict[str, str]] = []
    tables: List[List[List[str]]] = []

@app.post("/process-file", response_model=FileResponse)
async def process_file(file: UploadFile = File(...)):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        temp_file_path = temp_file.name
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
    
    try:
        content = processor.process_file(temp_file_path)
    finally:
        os.remove(temp_file_path)
    
    if "error" in content:
        raise HTTPException(status_code=400, detail=content["error"])
    
    return content
