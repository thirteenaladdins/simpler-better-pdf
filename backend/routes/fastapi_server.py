# fmt: off

from database.models import Base
from database.db import engine
import time
import os
import logging
import uuid
import datetime
import base64
import json
import io
import sys
from s3_tools.upload_to_s3 import upload_to_s3, fetch_file_from_s3, create_document
from database.models import Base, Document
from database.db import get_db
from sqlalchemy.orm import Session

# FAST API
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from routes.fastapi_ocr import ocr_router

# LOGGING
from logging_utils.logger import LoggingMiddleware, log_processed_data
from logging_utils.database_handler import DatabaseLogHandler

# PROCESSING
from luxury_goods import extract_luxury_goods_data
from cct_processing.map_to_cct_json import map_df_to_cct_json
from siemens import Siemens
from als_header.pdf_add_header_fixed import add_header_footer
from processing.file_processing import resave_pdf
from services import process_als_header, process_als_header_smaller_doc

from starlette.requests import Request

from typing import Optional

from dotenv import load_dotenv

# fmt: on

# TODO: equivalent
# from werkzeug.utils import secure_filename
# TODO: fastAPI equivalent?
# from routes.ocr import ocr_blueprint
# TODO: add secret key generation?

# Load the .env file
load_dotenv()

app = FastAPI()

# Create the database tables (for SQLite, in production you might use migrations)
Base.metadata.create_all(bind=engine)

# Include the router
app.include_router(ocr_router)

# TODO: adjust origins for test and prod
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


# Optionally initialize Colorama for Windows support:
# from colorama import init, Fore, Style
# init(autoreset=True)

# Create or get a dedicated logger
logger = logging.getLogger("access_logger")
logger.setLevel(logging.INFO)
logger.handlers.clear()

# Define a custom formatter with ANSI color and bold codes
# \033[1m = bold, \033[0m = reset, \033[94m = blue, \033[95m = magenta
formatter = logging.Formatter(
    "\n\033[1m[%(asctime)s]\033[0m \033[94m[%(levelname)s]\033[0m \033[95m[%(name)s]\033[0m %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

# Set up a stream handler that outputs to STDOUT
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Middleware to log detailed request/response information with color formatting


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = uuid.uuid4()  # Unique identifier for the request
    client_ip = request.client.host
    start_time = time.time()

    # Build the START message with bold labels and color
    start_message = (
        f"\033[1;32m[{request_id}] START\033[0m\n"
        f"   \033[1mMethod     :\033[0m {request.method}\n"
        f"   \033[1mURL        :\033[0m {request.url}\n"
        f"   \033[1mClient IP  :\033[0m {client_ip}\n"
        f"   \033[1mUser-Agent :\033[0m {request.headers.get('user-agent')}\n"
    )
    logger.info(start_message)

    response = await call_next(request)
    duration = time.time() - start_time

    # Build the END message similarly, highlighting status and duration
    end_message = (
        f"\033[1;31m[{request_id}] END\033[0m\n"
        f"   \033[1mMethod     :\033[0m {request.method}\n"
        f"   \033[1mURL        :\033[0m {request.url}\n"
        f"   \033[1mStatus     :\033[0m {response.status_code}\n"
        f"   \033[1mDuration   :\033[0m {duration:.2f} sec\n"
    )
    logger.info(end_message)
    return response

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

        # print(f"File saved at {filepath}")

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
async def process_pdf(file: UploadFile = File(...), option: Optional[str] = Form(None), db: Session = Depends(get_db)):
    # Check if file is attached
    if file is None:
        return JSONResponse(content={"error": "No file attached in request"}, status_code=400)

    # Check if form option is provided
    if option is None:
        return JSONResponse(content={"error": "Missing form option"}, status_code=400)

    # Read file content
    file_content = await file.read()
    file_name = file.filename

    # print(file_name)

    # Processing the file based on the option provided

    if option == "ALS Header New":
        processed_file = process_als_header(file_name, file_content, option)
        return processed_file

    elif option == "ALS Header 2":
        processed_file = process_als_header_smaller_doc(
            file_name, file_content, option)

        data = json.loads(processed_file.body)
        # Decode base64 to bytes
        pdf_bytes = base64.b64decode(data['url'])
        # Upload the file bytes to S3 and get a presigned URL
        # presigned_url = upload_to_s3(pdf_bytes)

        # this returns the doc_uuid
        doc_uuid, presigned_url = create_document(pdf_bytes)

        # add data to db here

        # Create a new document record in the database
        new_document = Document(
            filename=file_name,
            filetype="application/pdf",
            presigned_url=presigned_url,
            # FIXME: replace with actual expiration time
            # expires_at=datetime.datetime.now(
            #     datetime.timezone.utc) + datetime.timedelta(hours=1),
            id=doc_uuid,
            s3_key=doc_uuid  # Replace with the actual S3 key value
        )

        db.add(new_document)
        db.commit()

        # Add the presigned_url to the data dictionary
        data["presignedUrl"] = presigned_url

        # Should I get the object key from s3 instead?
        data["docId"] = doc_uuid

        # Return a JSON response containing both processed_file data and presigned_url
        return JSONResponse(content=data)

    # TODO: auto-save files for Raft
    elif option == "Re-Save PDF":
        # print(option, flush=True)
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


@app.get("/api/document/{doc_id}")
async def get_document(doc_id: str, db: Session = Depends(get_db)):
    # Fetch the document from the database
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Check if the presigned URL has expired
    # now = datetime.datetime.now(datetime.timezone.utc)
    # expires_in = (doc.expires_at - now).total_seconds()
    # if expires_in <= 0:
    #     raise HTTPException(status_code=410, detail="Presigned URL expired")
    # Optionally, you could generate a new presigned URL here and update the document.
    # For now, we'll just return an error.

    return JSONResponse(content={
        "doc_id": doc_id,
        "filename": doc.filename,
        "filetype": doc.filetype,
        "presignedUrl": doc.presigned_url
    })


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
