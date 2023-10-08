import os
import logging

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from luxury_goods import extract_luxury_goods_data
from siemens import Siemens
from als_header.pdf_add_header_footer import add_header_footer_to_pdf
from als_header.pdf_add_header import add_header_footer

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import os

from typing import Optional
import base64

import json
from dotenv import load_dotenv

# TODO: equivalent
# from werkzeug.utils import secure_filename
# TODO: fastAPI equivalent?
# from routes.ocr import ocr_blueprint
# TODO: add secret key generation?

# Load the .env file
load_dotenv()

app = FastAPI()

origins = ["http://localhost:5173",  # Replace with your local client's address
    "http://127.0.0.1:5173",
    "http://0.0.0.0:5173",]

# TODO: amend origins later

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow specific origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Constants
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp/")
ALLOWED_EXTENSIONS = {"pdf"}
MAX_UPLOAD_SIZE = 8 * 1024 * 1024  # 8 MB

# reorder this list. 
headers_list = ["tariff", "description", "quantity", "gross", "net", "value", "invoice"]

# Ensure UPLOAD_FOLDER exists
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except OSError as e:
    logging.error(f"Error creating directory {UPLOAD_FOLDER}: {str(e)}")


@app.get('/')
def home():
    return "Magic Extractor Deployed"


@app.get("/api/fetch_file/{filename:path}")
async def fetch_file(filename: str):
    als_header_dir = os.path.join(os.getcwd(), 'als_header')
    file_path = os.path.join(als_header_dir, filename)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="File not found")

    print(f"File path: {file_path}")

    return FileResponse(file_path)

# TODO: update this to process_file
@app.post("/api/process_file")
async def process_file(file: UploadFile = File(...), option: Optional[str] = Form(None)):
    # Check if file is attached
    if file is None:
        return JSONResponse(content={"error": "No file attached in request"}, status_code=400)

    # Check if form option is provided
    if option is None:
        return JSONResponse(content={"error": "Missing form option"}, status_code=400)
    
    # Read file content
    file_content = await file.read()
    file_name = file.filename

    # Processing the file based on the option provided
    if option == "Siemens Regex":
        processed_file = Siemens.extract_siemens(file_content)  # Make sure this function can handle bytes
        response_data = {
            "type": "csv",
            "data": processed_file.to_json(orient="records"),  # Assuming processed_file is a Pandas DataFrame
            "processType": "Siemens Regex"
        }
        return JSONResponse(content=response_data)

    elif option == "Luxury Goods":
        processed_file = extract_luxury_goods_data(file_content)  # Adjust function to handle bytes if necessary
        response_data = {
            "type": "csv",
            "data": processed_file.to_json(orient="records"),  # Assuming processed_file is a Pandas DataFrame
            "processType": "Luxury Goods"
        }
        return JSONResponse(content=response_data)

    else:
        return JSONResponse(content={"error": "Invalid form option"}, status_code=400)


@app.post("/api/process_pdf")
async def process_pdf(file: UploadFile = File(...), option: Optional[str] = Form(None)):
    # Check if file is attached
    if file is None:
        return JSONResponse(content={"error": "No file attached in request"}, status_code=400)

    # Check if form option is provided
    if option is None:
        return JSONResponse(content={"error": "Missing form option"}, status_code=400)

    # Read file content
    file_content = await file.read()
    file_name = file.filename

    # Processing the file based on the option provided
    if option == "ALS Header":
        # Process the file
        processed_file = add_header_footer_to_pdf(file_name, file_content)  # Ensure this function handles bytes
        response_data = {
            "type": "pdf",
            "url": processed_file,  # Modify if necessary to represent the correct path or URL
            "processType": "ALS Header"
        }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        return JSONResponse(content=response_data)

    elif option == "ALS Header New":
        # Process the file
        processed_file = add_header_footer(file_name, file_content)  # Ensure this function handles bytes
        # Convert bytes to Base64 encoded string
        encoded_pdf = base64.b64encode(processed_file).decode('utf-8')
        response_data = {
            "type": "pdf",
            "url": encoded_pdf,
            "processType": "ALS Header New"
        }
        return JSONResponse(content=response_data)

    else:
        return JSONResponse(content={"error": "Invalid form option"}, status_code=400)
 

@app.get("/ping")
async def ping():
    return {"status": "success", "message": "pong"}