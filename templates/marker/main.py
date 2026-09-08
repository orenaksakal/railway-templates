"""Authenticated CPU PDF-to-Markdown API with bounded, random-name uploads."""
import asyncio, hmac, os, tempfile
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict, shutdown_models
from marker.output import text_from_rendered
KEY = os.environ["API_KEY"]
LIMIT = 32 * 1024 * 1024
models = {}
busy = asyncio.Lock()
@asynccontextmanager
async def lifespan(app):
    models.update(create_model_dict())
    yield
    shutdown_models(models)
app = FastAPI(lifespan=lifespan)
@app.middleware("http")
async def authenticate(request, call_next):
    if not hmac.compare_digest(request.headers.get("x-api-key", ""), KEY):
        return JSONResponse({"detail": "Unauthorized"}, status_code=401)
    return await call_next(request)
def convert(path):
    converter = PdfConverter(artifact_dict=models, config={"mode": "fast", "disable_ocr": True, "pdftext_workers": 1})
    rendered = converter(path)
    text, _, _ = text_from_rendered(rendered)
    return {"markdown": text, "metadata": rendered.metadata}
@app.post("/convert")
async def upload(file: UploadFile = File(...)):
    if busy.locked():
        await file.close()
        raise HTTPException(429, "A conversion is already running")
    async with busy:
        path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as target:
                path = target.name
                size = 0
                while chunk := await file.read(1024 * 1024):
                    if size == 0 and not chunk.startswith(b"%PDF-"):
                        raise HTTPException(415, "PDF required")
                    size += len(chunk)
                    if size > LIMIT: raise HTTPException(413, "Maximum upload is 32 MiB")
                    target.write(chunk)
            if size == 0: raise HTTPException(400, "Empty file")
            return await run_in_threadpool(convert, path)
        finally:
            await file.close()
            if path: Path(path).unlink(missing_ok=True)
