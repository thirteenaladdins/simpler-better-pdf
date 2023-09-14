import os
import logging
import json 
import pandas as pd
import fitz 

from luxury_goods import extract_luxury_goods_data
from siemens import Siemens
from als_header.pdf_add_header_footer import add_header_footer_to_pdf
from flask import (
    Flask,
    jsonify,
    request,
    redirect,
    Response,
    send_file,
    make_response  # moved from flask.helpers to simplify
)
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from routes.ocr import ocr_blueprint

# Load the .env file
load_dotenv()

# Constants
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp/")
ALLOWED_EXTENSIONS = {"pdf"}

# App Setup
app = Flask(__name__)

app.register_blueprint(ocr_blueprint, url_prefix='/ocr')

CORS(app, resources={r"/*": {"origins": "*"}})

# Fetch or create a secret key
SECRET_KEY_ENV_VAR = "FLASK_APP_SECRET_KEY"

def get_or_create_secret_key():
    # Attempt to fetch the secret key from environment variables
    secret_key = os.environ.get(SECRET_KEY_ENV_VAR)
    
    # If it doesn't exist, generate a new one and prompt the user to set it
    if not secret_key:
        secret_key = os.urandom(32).hex()  # Generate a 256-bit key and convert it to hexadecimal for easier handling
        print(f"Generated a new secret key: {secret_key}")
        print(f"Please set the environment variable {SECRET_KEY_ENV_VAR} for consistent secret key across restarts.")
        
    return secret_key

app.secret_key = get_or_create_secret_key()

# Ensure UPLOAD_FOLDER exists
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except OSError as e:
    logging.error(f"Error creating directory {UPLOAD_FOLDER}: {str(e)}")




# reorder this list. 
headers_list = ["tariff", "description", "quantity", "gross", "net", "value", "invoice"]

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size upto 8mb
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

# extensions that are allowed to be processed
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    # return ('', 204)
    return 'Magic Extractor api deployed'   

# TODO: CHANGE THIS
@app.route('/api/delete_file/<path:filename>')
def delete_file(filename):
    als_header_dir = os.path.join(os.getcwd(), 'als_header')
    file_path = os.path.join(als_header_dir, filename)
    os.remove(file_path)
    response = make_response('')
    return response

@app.route('/api/fetch_file/<path:filename>')
def fetch_file(filename):
    als_header_dir = os.path.join(os.getcwd(), 'als_header')
    file_path = os.path.join(als_header_dir, filename)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return make_response("File not found", 404)

    print(f"File path: {file_path}")

    return send_file(file_path)


@app.route("/api/processfile", methods=["POST"])
def process():
    if request.method == "POST":
        print(request.files)
        if "file" not in request.files:
            print("No file attached in request")
            # return redirect(request.url)

            return redirect("/")
        
        # Check if form option is provided
        if "option" not in request.form or not request.form["option"]:
            error_response = {"error": "Missing form option"}
            return error_response, 400
            
        """From the immutablemultidict we can read the file data"""
        file = request.files["file"].read()
        file_name = request.files["file"].filename

        if request.form["option"] == "Siemens Regex":
            processed_file = Siemens.extract_siemens(file)
            response_data = {"type": "csv", "data": processed_file.to_json(orient="records")}

        elif request.form["option"] == "Luxury Goods":
            processed_file = extract_luxury_goods_data(file)
            response_data = {"type": "csv", "data": processed_file.to_json(orient="records")}

        elif request.form["option"] == "ALS Header":
            # returns the file name, side effect of writing the file to the 
            # script directory
            processed_file = add_header_footer_to_pdf(file_name, file)
            
            # response_data = {"type": "PDF", "data": processed_file}
            # run script, write file, fetch file from the server
            # sent to frontend

            # script_dir = os.path.dirname(os.path.abspath(__file__))

            # als_header_dir = os.path.join(script_dir, 'als_header')
            # # print(processed_file, font_dir)
            # header_file_path = als_header_dir + processed_file
            
            # this is just a string, but could I tag the type as application/pdf?
            return Response(response=processed_file, content_type='application/pdf')
        
            # return Response(response=processed_file, content_type='application/pdf')
            # return Response(response=pdf_data_base64, content_type='application/pdf')

        else: 
            # Return an error if form option is invalid
            error_response = {"error": "Invalid form option"}
            return error_response, 400

        return jsonify(response_data)

# PING when the website is loaded to start up 
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'success', 'message': 'pong'}), 200


@app.errorhandler(404)
def not_found(e):
    # return render_template("index.html")
    return "404"



