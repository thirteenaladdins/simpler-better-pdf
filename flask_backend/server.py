import os
from luxury_goods import extract_luxury_goods_data
from siemens import Siemens
from als_header.pdf_add_header_footer import add_header_footer_to_pdf

import base64

# TODO: migrate to FastAPI?

# from fastapi import FastAPI
# from mangum import Mangum

# fastapi_app = FastAPI()

# create a route that sends the information over from flask

# from send_data import dataframe_handler

from flask_cors import CORS, cross_origin
import json 

from flask import (
    Flask,
    jsonify,
    request,
    redirect,
    Response,
    send_file,
    send_from_directory,
    abort,
    url_for,
    render_template,
    flash,
)

from flask.helpers import make_response

from werkzeug.utils import secure_filename

# from dotenv import load_dotenv
# load_dotenv(find_dotenv())

# use pyPDF2 instead of fitz?

# from PyPDF2 import PdfFileReader, PdfFileWriter
# from processing.script import parse_args
# from processing.main import process_file
# from processing.Generation.export_template import generate_RX_template

import pandas as pd
import fitz 

# TODO: change to pymupdf - add existing scripts library


UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/tmp/"
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/downloads/"
OUTPUT_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/output/"

ALLOWED_EXTENSIONS = {"pdf"}

""" production build """
app = Flask(
    __name__,
    # static_url_path="",
    # static_folder="frontend/build",
    # template_folder="frontend/build",
)

# app.run(debug=True)

# comment out in production
CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)

# app.config["CORS_HEADERS"] = "Content-Type"
# errors.init_handler(app)
# cors = CORS(app, resource={r"/*": {"origins": "*"}})

# TODO ?
app.secret_key = os.urandom(12)


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except: 
    pass

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

# TODO: add all the checks and balances here
# so pass the file to this route on the backend

# we ping the api once per file and wait until each file has been processed, ,

# http://localhost:591/api/fetch_file/2022_9_20800.PDF_modified.pdf

# I want to remove the file from the directory after
# is this a security risk?
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


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 3000))
#     app.run(threaded=True, host="0.0.0.0", port=port)

# TODO these files are in the form 
        # if request.form["options"] == "CSV":
        #     # TODO do we return the file from here as json?

        #     # resp = make_response(processed_file.to_csv())
            
        #     if isinstance(processed_file, list):
        #         # row_json_data = json.dumps(process_file)
        #         # return row_json_data
        #         print(processed_file)
        #         return json.dumps(processed_file)

        #     else:
        #         print(type(processed_file))
        #         row_json_data = processed_file.to_json(orient="records")
        #         return row_json_data

        # TODO add a simpler way to - to what? not even sure what we're rendering here. 
        # return "Hello there"


