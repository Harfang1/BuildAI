from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from pathlib import Path
import unicodedata
import urllib.parse

app = FastAPI(title="File Server", description="Serve PDF documents and course files")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory where files are stored (can be overridden by environment variable)
FILES_DIR = os.getenv("FILES_DIR", "/app/files")


def find_file(identifier: str) -> Path | None:
    files_path = Path(FILES_DIR)
    if not files_path.exists():
        return None

    decoded = urllib.parse.unquote(identifier).strip()
    base_name = os.path.basename(decoded)
    stem = Path(base_name).stem

    # 1. Exact match with filename
    exact = files_path / base_name
    if exact.is_file():
        return exact

    # 2. Match with .pdf added
    with_pdf = files_path / f"{base_name}.pdf"
    if with_pdf.is_file():
        return with_pdf

    # 3. Match stem + .pdf
    stem_pdf = files_path / f"{stem}.pdf"
    if stem_pdf.is_file():
        return stem_pdf

    # 4. Glob match by stem.* or base_name.*
    matches = list(files_path.glob(f"{stem}.*")) or list(files_path.glob(f"{base_name}.*"))
    if matches:
        pdf_matches = [m for m in matches if m.suffix.lower() == ".pdf"]
        return pdf_matches[0] if pdf_matches else matches[0]

    # 5. Fuzzy match (normalized characters)
    def normalize_str(s: str) -> str:
        s = unicodedata.normalize("NFKD", s)
        s = "".join(c for c in s if not unicodedata.combining(c))
        return s.lower().replace("_", " ").replace("-", " ").strip()

    norm_target = normalize_str(stem)
    candidates = []
    for f in files_path.iterdir():
        if not f.is_file():
            continue
        norm_file = normalize_str(f.stem)
        if norm_target == norm_file:
            return f
        if norm_target in norm_file or norm_file in norm_target:
            candidates.append(f)

    if candidates:
        pdf_cand = [c for c in candidates if c.suffix.lower() == ".pdf"]
        return pdf_cand[0] if pdf_cand else candidates[0]

    return None


@app.get("/")
async def root():
    return {
        "message": "File Server API",
        "usage": "GET /download/{filename} to view/download a PDF file"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/download/{file_identifier:path}")
@app.get("/pdf/{file_identifier:path}")
async def download_file(file_identifier: str):
    """
    Download or view a PDF by filename, stem, or hash code.
    """
    target = find_file(file_identifier)
    if not target:
        raise HTTPException(
            status_code=404,
            detail=f"No document found for '{file_identifier}'"
        )

    is_pdf = target.suffix.lower() == ".pdf"
    media_type = "application/pdf" if is_pdf else "application/octet-stream"
    encoded_filename = urllib.parse.quote(target.name)

    return FileResponse(
        path=str(target),
        filename=target.name,
        media_type=media_type,
        headers={
            "Content-Disposition": f"inline; filename*=UTF-8''{encoded_filename}",
            "Access-Control-Allow-Origin": "*",
        }
    )


@app.get("/list")
async def list_files():
    try:
        files_path = Path(FILES_DIR)
        if not files_path.exists():
            return {"files": [], "message": "Files directory does not exist"}

        files = [f.name for f in files_path.iterdir() if f.is_file()]
        return {
            "files": sorted(files),
            "count": len(files),
            "directory": FILES_DIR
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
