# services.py
import base64
from als_header.pdf_add_header_fixed import add_header_footer
from fastapi.responses import JSONResponse


def process_als_header(file_name, file_content, option):
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


# def process_re_save_pdf(file_name, file_content):
#     # ...
#     return processed_file
