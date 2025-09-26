from fastapi import APIRouter, UploadFile, Form, HTTPException
from pathlib import Path
from app.services.files import save_upload_file
from app.services.rag import process_document

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload(document_id: str = Form(...), file: UploadFile = None):
    if file is None:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Save uploaded file with original name
    saved_path = save_upload_file(file, UPLOAD_DIR)
    print(f"DEBUG saved_path: {saved_path}")  # Debug: check path

    # Check extension
    suffix = Path(saved_path).suffix.lower()
    if suffix not in [".pdf", ".txt"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{suffix}'. Only PDF and TXT are allowed."
        )

    # Process document
    try:
        success = await process_document(document_id, str(saved_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {e}")

    return {"status": "ok" if success else "failed"}
