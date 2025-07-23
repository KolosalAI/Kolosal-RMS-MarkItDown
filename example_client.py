"""
Example client script to demonstrate how to use the Kolosal RMS MarkItDown API

This script shows how to make requests to the API endpoints from Python.
"""

import requests
import os
import json

# API base URL
BASE_URL = "http://localhost:8000"

def upload_file(endpoint: str, file_path: str) -> dict:
    """
    Upload a file to the specified endpoint
    
    Args:
        endpoint: API endpoint (e.g., '/parse_pdf')
        file_path: Path to the file to upload
        
    Returns:
        dict: API response
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    try:
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file)}
            response = requests.post(f"{BASE_URL}{endpoint}", files=files)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"HTTP {response.status_code}",
                    "detail": response.text
                }
    except Exception as e:
        return {"error": str(e)}

def check_health() -> dict:
    """Check API health status"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_api_info() -> dict:
    """Get API information"""
    try:
        response = requests.get(f"{BASE_URL}/")
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    """Main function to demonstrate API usage"""
    print("🚀 Kolosal RMS MarkItDown API Client Demo")
    print("=" * 50)
    
    # Check health
    print("\n1. Checking API health...")
    health = check_health()
    print(f"Health Status: {health}")
    
    # Get API info
    print("\n2. Getting API information...")
    info = get_api_info()
    print(f"API Info: {json.dumps(info, indent=2)}")
    
    # Example file paths (update these with actual files)
    examples = [
        ("/parse_pdf", "example.pdf"),
        ("/parse_docx", "example.docx"),
        ("/parse_xlsx", "example.xlsx"),
        ("/parse_pptx", "example.pptx"),
        ("/parse_html", "example.html"),
    ]
    
    print("\n3. Testing file parsing endpoints...")
    print("Note: Update file paths in the script to test with actual files")
    
    for endpoint, file_path in examples:
        print(f"\n📄 Testing {endpoint} with {file_path}")
        
        if os.path.exists(file_path):
            result = upload_file(endpoint, file_path)
            if "error" not in result:
                print(f"✅ Success! Converted {result['filename']}")
                print(f"📝 Title: {result['title']}")
                print(f"📊 File size: {result['metadata']['file_size']} bytes")
                print(f"🔤 Markdown preview (first 200 chars):")
                print(result['markdown_content'][:200] + "...")
            else:
                print(f"❌ Error: {result['error']}")
        else:
            print(f"⚠️  File not found: {file_path} (skipping)")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("\nTo test with your own files:")
    print("1. Update the file paths in this script")
    print("2. Make sure the API server is running on http://localhost:8000")
    print("3. Run this script again")

if __name__ == "__main__":
    main()
