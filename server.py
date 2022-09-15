import os
from main import extract_luxury_goods_data
from siemens import Siemens

# create a route that sends the information over from flask

# from send_data import dataframe_handler

from flask_cors import CORS, cross_origin
import json 

from flask import (
    Flask,
    jsonify,
    request,
    redirect,
    url_for,
    render_template,
    send_from_directory,
    Response,
    flash,
)

from flask.helpers import make_response

from werkzeug.utils import secure_filename

# from dotenv import load_dotenv
# load_dotenv(find_dotenv())

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

# Is this necessary?
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


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

# we ping the api once per file and wait until each file has been processed

@app.route("/api/processfile", methods=["POST"])
def process():
    if request.method == "POST":
        
        # run for loop for each file that is posted
        
        print(request.files)
        if "file" not in request.files:
            print("No file attached in request")
            # return redirect(request.url)

            return redirect("/")
        """From the immutablemultidict we can read the file data"""
        file = request.files["file"].read()

        """ Process the file here - return the dataframe """
        if request.form["option"] == "Siemens":
            processed_file = None
            processed_file = Siemens.extract_siemens(file)

        elif request.form["option"] == "Luxury Goods":
            processed_file = None
            processed_file = extract_luxury_goods_data(file)


        return processed_file.to_json(orient="records")
        

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


