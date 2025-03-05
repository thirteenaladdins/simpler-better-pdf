# fmt: off
import time
import os
import logging
import uuid
import datetime
import base64
import json
import sys

# FAST API
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse

# PROCESSING
from processing.file_processing import resave_pdf
from services import process_als_header, process_als_header_smaller_doc

from starlette.requests import Request

from typing import Optional

from dotenv import load_dotenv

# fmt: on

# Load the .env file
load_dotenv()

app = FastAPI()


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


# @app.get('/')
# def home():
@app.get('/', response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Simpler Better PDF Backend</title>
      <p>Simpler Better PDF Backend</p>
      <style>
        html, body {
          height: 100%;
          margin: 0;
          background-color: #242F3F;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          text-align: center;
          font-family: sans-serif;
        }
        p {
            color: #fff;
        }
        .loader {
          display: inline-block;
          width: 50px;
          height: 50px;
          position: relative;
          border: 4px solid #fff;
          border-radius: 50%;
          animation: loader-rotate 2s infinite ease;
        }
        .loader-inner {
          position: absolute;
          left: 50%;
          transform: translateX(-50%);
          width: 4px;
          background-color: #fff;
          animation: loader-fill 2s infinite ease-in;
        }
        /* Bottom line: positioned at the bottom */
        .loader-inner.bottom {
          bottom: 0;
        }
        /* Top line: positioned at the top with a delay */
        .loader-inner.top {
          top: 0;
          animation-delay: 1s;
        }
        @keyframes loader-rotate {
          0% {
            transform: rotate(0deg);
          }
          25% {
            transform: rotate(180deg);
          }
          50% {
            transform: rotate(180deg);
          }
          75% {
            transform: rotate(360deg);
          }
          100% {
            transform: rotate(360deg);
          }
        }
        @keyframes loader-fill {
          0% {
            height: 0%;
          }
          25% {
            height: 0%;
          }
          50% {
            height: 100%;
          }
          75% {
            height: 100%;
          }
          100% {
            height: 0%;
          }
        }
      </style>
    </head>
    <body>
      <div class="loader">
        <div class="loader-inner bottom"></div>
        <div class="loader-inner top"></div>
      </div>
    </body>
    </html>
 """


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

    # print(file_name)

    # Processing the file based on the option provided

    if option == "ALS Header New":
        processed_file = process_als_header(file_name, file_content, option)

        data = json.loads(processed_file.body)
        # Decode base64 to bytes
        pdf_bytes = base64.b64decode(data['url'])

        doc_uuid = str(uuid.uuid4())

        # Construct the full file path
        folder = '/tmp'

        # generate file name

        filename = f'{doc_uuid}.pdf'
        filepath = os.path.join(folder, filename)

        print(filename)

        if not os.path.exists(folder):
            os.makedirs(folder)

        # Ensure pdf_bytes is not empty
        if not pdf_bytes:
            raise HTTPException(
                status_code=500, detail="Failed to process PDF content")

        # Write the PDF bytes to the file
        with open(filepath, 'wb') as f:
            f.write(pdf_bytes)

        with open(filepath, 'wb') as f:
            f.write(pdf_bytes)

            if os.path.exists(filepath):
                logger.info(
                    f"File successfully written to: {filepath}, size: {os.path.getsize(filepath)} bytes")
            else:
                logger.error("File does not exist after writing!")

        print(f"File written to: {filepath}")

        if not os.path.exists(filepath):
            print("File does not exist after writing!")

        data["docId"] = doc_uuid
        return JSONResponse(content=data)

    elif option == "ALS Header 2":
        processed_file = process_als_header_smaller_doc(
            file_name, file_content, option)

        data = json.loads(processed_file.body)
        # Decode base64 to bytes
        pdf_bytes = base64.b64decode(data['url'])

        doc_uuid = str(uuid.uuid4())

        # Construct the full file path
        folder = '/tmp'

        # generate file name

        filename = f'{doc_uuid}.pdf'
        filepath = os.path.join(folder, filename)

        print(filename)

        if not os.path.exists(folder):
            os.makedirs(folder)

        # Ensure pdf_bytes is not empty
        if not pdf_bytes:
            raise HTTPException(
                status_code=500, detail="Failed to process PDF content")

        # Write the PDF bytes to the file
        with open(filepath, 'wb') as f:
            f.write(pdf_bytes)

        print(f"File written to: {filepath}")

        if not os.path.exists(filepath):
            print("File does not exist after writing!")

        data["docId"] = doc_uuid

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
async def get_document(doc_id: str):
    # Construct the full file path. Adjust the directory as needed.
    filepath = os.path.join("/tmp", f"{doc_id}.pdf")

    if not os.path.exists(filepath):
        logger.error(f"File not found for doc_id: {doc_id}")
        raise HTTPException(status_code=404, detail="File not found")

    # Return the file as a response with the appropriate media type
    return FileResponse(
        path=filepath,
        media_type="application/pdf",
        # filename=f"{doc_id}.pdf",
        headers={"Content-Disposition": f"inline; filename={doc_id}.pdf"}
    )


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
