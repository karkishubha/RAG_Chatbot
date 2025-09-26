from pathlib import Path
from PyPDF2 import PdfReader
from fastapi import UploadFile

def save_upload_file(upload_file: UploadFile, destination_folder: Path) -> Path:
    """
    Save a FastAPI UploadFile to disk while preserving its original filename.
    Returns the full path of the saved file.
    """
    
    destination_folder.mkdir(parents=True, exist_ok=True)

    
    destination = destination_folder / upload_file.filename

    
    with destination.open("wb") as f:
        f.write(upload_file.file.read())

    return destination  

def extract_text_from_pdf_or_txt(file_path: str) -> str:
    """
    Extract text from a PDF or TXT file.
    - PDFs: uses PyPDF2
    - TXT: tries UTF-8, falls back to Latin-1 if needed
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = p.suffix.lower()

    if suffix == ".pdf":
        # Extract text from PDF
        reader = PdfReader(str(p))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()

    elif suffix == ".txt":
        
        try:
            return p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return p.read_text(encoding="latin-1")

    else:
        raise ValueError(f"Unsupported file type '{suffix}'. Only PDF and TXT are allowed.")
