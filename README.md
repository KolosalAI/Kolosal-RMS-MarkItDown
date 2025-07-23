# Kolosal RMS MarkItDown Server

A FastAPI-based server that provides REST API endpoints for converting various file formats to Markdown using Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) library.

## 🚀 Features

- **Multiple File Format Support**: Convert PDF, DOCX, XLSX, PPTX, and HTML files to Markdown
- **Async & Thread-Safe**: Built with FastAPI for high performance and concurrent request handling
- **Docker Ready**: Fully containerized with Docker and Docker Compose support
- **REST API**: Clean RESTful endpoints for easy integration
- **Error Handling**: Comprehensive error handling and logging
- **Health Checks**: Built-in health check endpoints
- **CORS Enabled**: Cross-origin resource sharing support

## 📋 Supported File Formats

| Format | Endpoint | File Extensions |
|--------|----------|----------------|
| PDF | `/parse_pdf` | `.pdf` |
| Word Documents | `/parse_docx` | `.docx` |
| Excel Spreadsheets | `/parse_xlsx` | `.xlsx`, `.xls` |
| PowerPoint Presentations | `/parse_pptx` | `.pptx`, `.ppt` |
| HTML Files | `/parse_html` | `.html`, `.htm` |

## 🛠 Installation

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Kolosal-RMS-MarkItDown
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**:
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

### Docker

1. **Build and run with Docker**:
   ```bash
   docker build -t markitdown-api .
   docker run -p 8000:8000 markitdown-api
   ```

2. **Or use Docker Compose**:
   ```bash
   docker-compose up -d
   ```

## 📖 API Usage

### Interactive Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example API Calls

#### Convert PDF to Markdown
```bash
curl -X POST "http://localhost:8000/parse_pdf" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.pdf"
```

#### Convert Word Document to Markdown
```bash
curl -X POST "http://localhost:8000/parse_docx" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.docx"
```

#### Convert Excel to Markdown
```bash
curl -X POST "http://localhost:8000/parse_xlsx" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@spreadsheet.xlsx"
```

#### Convert PowerPoint to Markdown
```bash
curl -X POST "http://localhost:8000/parse_pptx" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@presentation.pptx"
```

#### Convert HTML to Markdown
```bash
curl -X POST "http://localhost:8000/parse_html" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@webpage.html"
```

### Response Format

All endpoints return a JSON response with the following structure:

```json
{
  "success": true,
  "filename": "document.pdf",
  "markdown_content": "# Document Title\n\nDocument content in markdown format...",
  "title": "Document Title",
  "metadata": {
    "original_filename": "document.pdf",
    "file_size": 1024576,
    "mime_type": "application/pdf"
  }
}
```

## 🏥 Health Check

The server provides a health check endpoint:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "markitdown-api"
}
```

## ⚡ Performance Features

- **Async Processing**: All file operations are handled asynchronously
- **Thread Pool**: CPU-intensive conversions run in a dedicated thread pool
- **Concurrent Requests**: Supports multiple simultaneous file conversions
- **Memory Efficient**: Uses streaming for file processing
- **Error Recovery**: Graceful error handling without server crashes

## 🔧 Configuration

The server can be configured through environment variables:

- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)
- `LOG_LEVEL`: Logging level (default: `info`)

## 🐳 Docker Configuration

### Build Image
```bash
docker build -t kolosal-markitdown-api .
```

### Run Container
```bash
docker run -d \
  --name markitdown-api \
  -p 8000:8000 \
  kolosal-markitdown-api
```

### Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

This project is built using [Microsoft's MarkItDown](https://github.com/microsoft/markitdown) library, which provides the core functionality for converting various file formats to Markdown.

- **MarkItDown**: https://github.com/microsoft/markitdown
- **Microsoft**: For creating and maintaining the MarkItDown library
- **FastAPI**: For the excellent async web framework
- **Uvicorn**: For the ASGI server implementation

## 📞 Support

For support and questions, please:
1. Check the [documentation](http://localhost:8000/docs)
2. Search existing issues in the repository
3. Create a new issue if needed

---

**Kolosal Inc** - Retrieval Management Service Implementation
