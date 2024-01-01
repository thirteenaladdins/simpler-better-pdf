import os
import logging
import uuid
import datetime
import base64
import json
import io

# FAST API
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse

# LOGGING
from logging_utils.logger import LoggingMiddleware, log_processed_data
from logging_utils.database_handler import DatabaseLogHandler

# PROCESSING
from luxury_goods import extract_luxury_goods_data
from cct_processing.map_to_cct_json import map_df_to_cct_json
from siemens import Siemens
from als_header.pdf_add_header_footer import add_header_footer_to_pdf
# from als_header.pdf_add_header import add_header_footer
from als_header.pdf_add_header_fixed import add_header_footer
from processing.pdf_processing import resave_pdf

from starlette.requests import Request

from typing import Optional

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

app.add_middleware(LoggingMiddleware)

# Constants
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "tmp/")
ALLOWED_EXTENSIONS = {"pdf"}
MAX_UPLOAD_SIZE = 8 * 1024 * 1024  # 8 MB

# reorder this list.
headers_list = ["tariff", "description",
                "quantity", "gross", "net", "value", "invoice"]

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
# what is the difference between process_file and process_pdf
# not clear

# returns CSV


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
        # Make sure this function can handle bytes
        processed_file = Siemens.extract_siemens(file_content)
        response_data = {
            "type": "csv",
            # Assuming processed_file is a Pandas DataFrame
            "data": processed_file.to_json(orient="records"),
            "processType": "Siemens Regex"
        }

        # log_processed_data(file.filename, option, response_data)
        return JSONResponse(content=response_data)

    elif option == "Luxury Goods":
        # Adjust function to handle bytes if necessary
        processed_file = extract_luxury_goods_data(file_content)
        converted_file = map_df_to_cct_json(processed_file)

        folder = 'tmp'
        # generate file name

        myuuid = uuid.uuid4()
        # UUID
        filename = f'VECTORAI_LUXURY_GOODS_{myuuid}.json'
        # save data to file
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Construct the full file path
        filepath = os.path.join(folder, filename)

        # Write the data to a JSON file
        with open(filepath, 'w') as json_file:

            json.dump(converted_file, json_file)

        print(f"File saved at {filepath}")

        response_data = {
            "type": "csv",
            # Assuming processed_file is a Pandas DataFrame
            "data": processed_file.to_json(orient="records"),
            "processType": "Luxury Goods"
        }

        # log_processed_data(file.filename, option, response_data)

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

    print(file_name)

    # Processing the file based on the option provided

    if option == "ALS Header New":
        # Process the file
        # Ensure this function handles bytes

        processed_file = add_header_footer(file_name, file_content)
        # Convert bytes to Base64 encoded string

        encoded_pdf = base64.b64encode(processed_file).decode('utf-8')
        response_data = {
            "type": "application/pdf",
            "url": encoded_pdf,
            "processType": option,
            "fileName": file_name
        }
        return JSONResponse(content=response_data)

    # TODO: auto-save files for Raft
    elif option == "Re-Save PDF":
        print(option, flush=True)
        processed_file = resave_pdf(file_name, file_content)
        # Convert bytes to Base64 encoded string

        encoded_pdf = base64.b64encode(processed_file).decode('utf-8')
        response_data = {
            "type": "application/pdf",
            "url": encoded_pdf,
            "processType": option,
            "fileName": file_name
        }
        return JSONResponse(content=response_data)

    else:
        return JSONResponse(content={"error": "Invalid form option"}, status_code=400)


@app.get("/ping")
async def ping(request: Request):
    # Get IP address and user agent from the request
    ip_address = request.client.host
    user_agent = request.headers.get('user-agent')
    access_time = datetime.datetime.now()

    # get from .env
    environment = "dev"  # adjust accordingly based on your setup

    # Log the access details
    try:
        DatabaseLogHandler.log_access(
            access_time, ip_address, user_agent, environment)
        # notify me when someone uses the application

    except Exception as e:
        # Consider logging the exception here for debugging purposes
        pass

    return {"status": "success", "message": "pong"}
