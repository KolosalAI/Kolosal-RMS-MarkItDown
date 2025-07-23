import asyncio
import io
import logging
import mimetypes
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from markitdown import MarkItDown
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Kolosal RMS MarkItDown API",
    description="A FastAPI server for converting various file formats to Markdown using Microsoft's MarkItDown library",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thread pool for CPU-bound operations
executor = ThreadPoolExecutor(max_workers=4)

# Initialize MarkItDown instance
markitdown = MarkItDown(enable_plugins=False)

def convert_file_sync(file_content: bytes, filename: str, is_html: bool = False) -> Dict[str, Any]:
    """
    Synchronous file conversion function to be run in thread pool
    """
    try:
        if is_html:
            # For HTML files, use the content directly as MarkItDown can handle it
            file_stream = io.BytesIO(file_content)
            file_stream.name = filename
        else:
            # For non-HTML files (PDF, DOCX, XLSX, PPTX), ensure proper BytesIO handling
            file_stream = io.BytesIO(file_content)
            file_stream.name = filename
            # Ensure we're at the beginning of the stream
            file_stream.seek(0)
        
        # Convert using MarkItDown
        result = markitdown.convert_stream(file_stream)
        
        return {
            "success": True,
            "filename": filename,
            "markdown_content": result.text_content,
            "title": result.title or filename,
            "metadata": {
                "original_filename": filename,
                "file_size": len(file_content),
                "mime_type": mimetypes.guess_type(filename)[0],
                "file_type": "html" if is_html else "binary"
            }
        }
    except Exception as e:
        logger.error(f"Error converting file {filename}: {str(e)}")
        raise e

async def process_file(file: UploadFile, expected_types: list, is_html: bool = False) -> Dict[str, Any]:
    """
    Process uploaded file asynchronously with thread safety
    """
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    # Check file extension
    file_ext = file.filename.lower().split('.')[-1] if '.' in file.filename else ''
    if file_ext not in expected_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Expected: {', '.join(expected_types)}"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        if not file_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file provided"
            )
        
        # Process in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor, 
            convert_file_sync, 
            file_content, 
            file.filename,
            is_html
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Kolosal RMS MarkItDown API",
        "description": "Convert various file formats to Markdown using Microsoft's MarkItDown library",
        "version": "1.0.0",
        "endpoints": [
            "/parse_pdf - Convert PDF files to Markdown",
            "/parse_docx - Convert Word documents to Markdown", 
            "/parse_xlsx - Convert Excel files to Markdown",
            "/parse_pptx - Convert PowerPoint presentations to Markdown",
            "/parse_html - Convert HTML files to Markdown"
        ],
        "credits": "Built using Microsoft MarkItDown: https://github.com/microsoft/markitdown"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "markitdown-api"}

@app.post("/parse_pdf")
async def parse_pdf(file: UploadFile = File(...)):
    """
    Convert PDF files to Markdown
    """
    result = await process_file(file, ['pdf'])
    return JSONResponse(content=result, status_code=200)

@app.post("/parse_docx")
async def parse_docx(file: UploadFile = File(...)):
    """
    Convert Word documents to Markdown
    """
    result = await process_file(file, ['docx'])
    return JSONResponse(content=result, status_code=200)

@app.post("/parse_xlsx")
async def parse_xlsx(file: UploadFile = File(...)):
    """
    Convert Excel files to Markdown
    """
    result = await process_file(file, ['xlsx', 'xls'])
    return JSONResponse(content=result, status_code=200)

@app.post("/parse_pptx")
async def parse_pptx(file: UploadFile = File(...)):
    """
    Convert PowerPoint presentations to Markdown
    """
    result = await process_file(file, ['pptx', 'ppt'])
    return JSONResponse(content=result, status_code=200)

@app.post("/parse_html")
async def parse_html(file: UploadFile = File(...)):
    """
    Convert HTML files to Markdown
    """
    result = await process_file(file, ['html', 'htm'], is_html=True)
    return JSONResponse(content=result, status_code=200)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error occurred"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
