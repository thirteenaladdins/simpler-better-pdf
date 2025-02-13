# Import the required modulesimport io
import base64
import io
import os
import sys
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Frame, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# import textwrap

# TODO: add standard footer
footer_text = """All business transacted in accordance with the Standard Trading Conditions of the British International Freight Association Ltd (Latest Edition)."""

footer_text_2 = """IMPORTANT NOTE:- for contracts subject to the CMR Convention, for the purpose of Articles 37 and 38 of that Convention the party to whom"""

# NOTE: change to ALS
footer_text_3 = """ALS Customs Services Ltd contracts a movement shall be treated as the responsible carrier in addition to the actual responsible carrier.
Registered Office: Liverpool Road, Eccles, Manchester, England, M30 7RF. Reg No. 2625304. VAT No. GB 570 4871 30
A MEMBER OF RHENUS LOGISTICS"""

# Register the Open Sans font
pdfmetrics.registerFont(TTFont('OpenSans', '../fonts/OpenSans-Regular.ttf'))
# header_text = "This is a header"


def draw_wrapped_line(canvas, text, length, x_pos, y_pos, y_offset):
    """
    :param canvas: reportlab canvas
    :param text: the raw text to wrap
    :param length: the max number of characters per line
    :param x_pos: starting x position
    :param y_pos: starting y position
    :param y_offset: the amount of space to leave between wrapped lines
    """
    if len(text) > length:
        wraps = textwrap.wrap(text, length)
        for x in range(len(wraps)):
            canvas.drawCentredString(x_pos, y_pos, wraps[x])
            y_pos -= y_offset
        y_pos += y_offset  # add back offset after last wrapped line
    else:
        canvas.drawCentredString(x_pos, y_pos, text)
    return y_pos


def draw_image_with_border(canvas, image_data, x, y, width=None, height=None, border_thickness=1, border_color=(0, 0, 0)):
    # Decode the image data
    decoded_image_data = base64.b64decode(image_data.split(',')[1])
    image_reader = ImageReader(io.BytesIO(decoded_image_data))
    img_width, img_height = image_reader.getSize()
    aspect_ratio = img_width / img_height

    if width is not None and height is not None:
        # Adjust the size to maintain aspect ratio
        if width / height > aspect_ratio:
            width = height * aspect_ratio
        else:
            height = width / aspect_ratio

    # Calculate the position to center the image on the page
    page_width, page_height = A4
    center_x = page_width / 2
    x = center_x - (width / 2)

    # Draw the border
    canvas.setStrokeColorRGB(*border_color)  # Set border color
    canvas.setLineWidth(border_thickness)  # Set border thickness

    # Draw rectangle for the border slightly larger than the image
    canvas.rect(x - border_thickness, y - height - border_thickness, width +
                2*border_thickness, height + 2*border_thickness, stroke=1, fill=0)

    # Draw the image
    canvas.drawImage(image_reader, x, y - height,
                     width=width, height=height, mask='auto')


def draw_image(canvas, image_data, x, y, width=None, height=None):
    decoded_image_data = base64.b64decode(image_data.split(',')[1])
    image_reader = ImageReader(io.BytesIO(decoded_image_data))
    img_width, img_height = image_reader.getSize()
    aspect_ratio = img_width / img_height

    if width is not None and height is not None:
        if width / height > aspect_ratio:
            width = height * aspect_ratio
            print(width)
        else:
            height = width / aspect_ratio
            print(height)

    page_width, page_height = A4
    center_x = page_width / 2

    # Calculate the position to place the image to center it on the page
    x = center_x - (width / 2)

    canvas.drawImage(ImageReader(image_reader), x, y - 172,
                     width=width, height=height, mask='auto')


# should be directory agnostic
als_header_dir = os.path.join(os.getcwd(), 'als_header')


def add_header_footer_smaller_doc(file_name, input_file):

    # Create a PdfFileWriter object to write the output file
    writer = PdfWriter()

    # input image file, then convert, then import into this script?
    # try:
    encoded_image_path = os.path.join(als_header_dir, 'als_logo.txt')
    with open(encoded_image_path, 'r') as f:
        encoded_image_data = f.read()
        # add prefix to image
        encoded_image_data = 'data:image/png;base64,' + encoded_image_data
    # except Exception as e:
    #     print(f"Error: {e}")
    #     sys.exit(1)

    try:
        reader = PdfReader(io.BytesIO(input_file))
        logging.info("PDF file read successfully")
    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error reading PDF file: {e}")
        sys.exit(1)

    # Loop through each page of the input file
    for page_num in range(len(reader.pages)):
        # Get the current page
        page = reader.pages[page_num]

        # Create a canvas object to draw the footer and header
        temp_pdf_path = f"temp_{page_num}.pdf"
        canvas_obj = canvas.Canvas(temp_pdf_path, pagesize=A4)

        # Get the page width and height
        page_width, page_height = A4

        # Draw the footer text at the bottom center of the page
        canvas_obj.setFont("OpenSans", 7)

        adjustment = 10
        # page_width and page_height are being passed in here
        draw_image(canvas_obj, encoded_image_data,
                   page_width, page_height - adjustment, 220, 180)

        # adjusted
        adjustment_value = 10
        draw_wrapped_line(canvas_obj, footer_text, 150,
                          page_width / 2, 62, 10)

        draw_wrapped_line(canvas_obj, footer_text_2,
                          150, page_width / 2, 52, 10)
        draw_wrapped_line(canvas_obj, footer_text_3,
                          150, page_width / 2, 42, 10)

        # Save the canvas object
        canvas_obj.save()

        # Merge the canvas object with the current page
        watermark = PdfReader(temp_pdf_path)
        page.merge_page(watermark.pages[0])

        # Add the modified page to the output file
        writer.add_page(page)
        os.remove(temp_pdf_path)

    output_stream = io.BytesIO()
    writer.write(output_stream)

    # Getting the PDF data from the BytesIO stream
    output_stream.seek(0)
    return output_stream.getvalue()


def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <pdf_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, 'rb') as file:
        pdf_content = file.read()

    output_pdf = add_header_footer_smaller_doc(file_path, pdf_content)
    # Save output_pdf to a file or process further...
    output_file_path = "modified_" + file_path.split('/')[-1]

    # Write the output PDF to a file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(output_pdf)

    print(f"Modified PDF saved as {output_file_path}")


if __name__ == "__main__":
    main()
