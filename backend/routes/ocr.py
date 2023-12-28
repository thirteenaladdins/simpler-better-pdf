import os
import logging
from flask import Blueprint, request, jsonify
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import base64

# Blueprint configuration
ocr_blueprint = Blueprint('ocr', __name__)

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf'}


# Utility function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ocr_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        return process_file(filepath)
    else:
        return jsonify({"error": "Unsupported file type"}), 400


def process_file(filepath):
    try:
        logging.info(f"Processing file: {filepath}")

        images = convert_from_path(filepath)
        ocr_results = []

        # Store the dimensions of the first image (representing the first page)
        first_page_dimensions = {
            "width": images[0].width,
            "height": images[0].height
        }

        # work with the results of a single page for now
        if images:
            image = images[0]
        # for image in images:
            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            # Convert the flat structure to the desired hierarchical format
            formatted_results = []
            for i in range(len(ocr_data["text"])):
                if ocr_data["text"][i].strip():  # only include non-empty strings
                    formatted_word_data = {
                        "bbox": {
                            "height": ocr_data["height"][i],
                            "left": ocr_data["left"][i],
                            "top": ocr_data["top"][i],
                            "width": ocr_data["width"][i]
                        },
                        "block_num": ocr_data["block_num"][i],
                        "conf": ocr_data["conf"][i],
                        "line_num": ocr_data["line_num"][i],
                        "page_num": ocr_data["page_num"][i],
                        "par_num": ocr_data["par_num"][i],
                        "text": ocr_data["text"][i]
                    }
                    formatted_results.append(formatted_word_data)

            ocr_results.extend(formatted_results)

        # we have to open the file here instead 
        with open(filepath, 'rb') as pdf_file:
            encoded_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')

        os.remove(filepath)  # remove the saved file
        logging.info(f"Processed and removed file: {filepath}")
        
        return jsonify({"data": ocr_results, "pdfBase64": encoded_pdf,
                         "dimensions": first_page_dimensions, "processType": "Annotate"})

    except Exception as e:
        logging.error(f"Error processing file: {filepath}. Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Change the function name and the argument type
def ocr_image_from_pil_image(image):
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    # Extract relevant data: text, bounding box, confidence...
    words_data = []
    for i in range(len(data['text'])):
        if data['text'][i]:  # Only process if text exists
            word_data = {
                'text': data['text'][i],
                'block_num': data['block_num'][i],
                'line_num': data['line_num'][i],
                'page_num': data['page_num'][i],
                'par_num': data['par_num'][i],
                'conf': data['conf'][i],
                'bbox': {  # changed the structure to have bbox as a dictionary
                    'left': data['left'][i],
                    'top': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i]
                }
            }
            words_data.append(word_data)

    return words_data
