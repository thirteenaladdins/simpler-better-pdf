# Import the required modules
from dotenv import load_dotenv
import os
import base64
import io
import sys
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.pdfgen import canvas
import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
# from reportlab.platypus import Frame, SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

# import textwrap


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


footer_text = """All business transacted in accordance with the Standard Trading Conditions of the British International Freight Association Ltd (Latest Edition)."""

footer_text_2 = """IMPORTANT NOTE:- for contracts subject to the CMR Convention, for the purpose of Articles 37 and 38 of that Convention the party to whom"""

footer_text_3 = """ALS Customs Services Ltd contracts a movement shall be treated as the responsible carrier in addition to the actual responsible carrier.
Registered Office: Liverpool Road, Eccles, Manchester, England, M30 7RF. Reg No. 2625304. VAT No. GB 570 4871 30
A MEMBER OF RHENUS LOGISTICS"""

# Get the current script's directory

font_file = "OpenSans-Regular.ttf"
font_path = os.getenv('FONT_PATH')
if font_path is None:
    raise ValueError(
        "Font path is not set. Please set the FONT_PATH environment variable.")
else:
    pass
    # Use font_path in your script

als_header_dir = os.path.join(os.getcwd(), 'als_header')

# # Define the font directory and file relative to the script's directory
# font_dir = os.path.join(als_header_dir, '..', 'fonts')
# font_file = "OpenSans-Regular.ttf"

# # Create the font path and register the font
# font_path = os.path.join(font_dir, font_file)
pdfmetrics.registerFont(TTFont("OpenSans", font_path))


# def add_header_footer(file_name, input_file):
def add_header_footer(file_name, input_file):
    # Create a PdfFileReader object to read the input file
    logging.info("Starting to add header and footer")
    try:
        reader = PdfReader(io.BytesIO(input_file))
        logging.info("PDF file read successfully")
    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error reading PDF file: {e}")
        sys.exit(1)

    # Create a PdfFileWriter object to write the output file
    writer = PdfWriter()

    # input image file, then convert, then import into this script?
    try:
        encoded_image_path = os.path.join(als_header_dir, 'output.txt')
        with open(encoded_image_path, 'r') as f:
            encoded_image_data = f.read()
            # add prefix to image
            encoded_image_data = 'data:image/png;base64,' + encoded_image_data
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Loop through each page of the input file
    for page_num in range(len(reader.pages)):
        # Get the current page
        page = reader.pages[page_num]

        # Create a canvas object to draw the footer and header using in-memory binary stream
        # packet = io.BytesIO()
        # canvas_obj = canvas.Canvas(packet, pagesize=A4)

        temp_pdf_path = f"temp_{page_num}.pdf"
        canvas_obj = canvas.Canvas(temp_pdf_path, pagesize=A4)

        # Get the page width and height
        page_width, page_height = A4

        # Draw the footer text at the bottom center of the page
        canvas_obj.setFont("OpenSans", 8)

        # Draw the image and footer texts
        draw_image(canvas_obj, encoded_image_data,
                   page_width, page_height, 220, 180)
        draw_wrapped_line(canvas_obj, footer_text, 150, page_width / 2, 64, 10)
        draw_wrapped_line(canvas_obj, footer_text_2,
                          150, page_width / 2, 54, 10)
        draw_wrapped_line(canvas_obj, footer_text_3,
                          150, page_width / 2, 44, 10)

        # Save the canvas object
        canvas_obj.save()
        # packet.seek(0)

        # Merge the canvas object with the current page
        # watermark = PdfReader(packet)

        watermark = PdfReader(temp_pdf_path)

        watermark_page = watermark.pages[0]
        watermark_page.merge_page(page)
        writer.add_page(watermark_page)
        os.remove(temp_pdf_path)

    output_file_path_2 = "before_stream_" + file_name
    # Write the modified content directly to a file
    with open(output_file_path_2, 'wb') as output_file:
        writer.write(output_file)

    print(f"Modified PDF 2s saved as {output_file_path_2}")

    # Write the modified content to an in-memory binary stream
    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)

    # Save the modified PDF to a file before returning
    output_file_path = "modified_stream_" + file_name

    with open(output_file_path, 'wb') as output_file:
        output_file.write(output_stream.getvalue())

    print(f"Modified PDF saved as {output_file_path}")

    return output_stream.getvalue()

    # does the backslash/forward slash depend on the os?
    # file_path = f'{als_header_dir}/{output_file_name}'

    # try:
    #     # create a temporary directory to write this to
    #     with open(file_path, "wb") as out:
    #         writer.write(out)

    #     if os.path.exists(file_path):
    #         print(f"File {output_file_name} created successfully at {file_path}")
    #     else:
    #         print(f"Error occurred while creating {output_file_name}")

    #     # now check if the file has been successfully created
    #     return output_file_name

    # except Exception as e:
    #     # Print an error message if an exception occurs
    #     print(f"Error occurred while creating {output_file_name}: {str(e)}")


def draw_image(canvas, image_data, x, y, width=None, height=None):
    decoded_image_data = base64.b64decode(image_data.split(',')[1])
    # save image temporarily
    # with open(f"temp_image_{2}.png", "wb") as img_file:
    #     img_file.write(decoded_image_data)

    image_reader = ImageReader(io.BytesIO(decoded_image_data))
    img_width, img_height = image_reader.getSize()
    aspect_ratio = img_width / img_height

    # Scaling
    if width is not None and height is not None:
        if width / height > aspect_ratio:
            width = height * aspect_ratio
            print(width)
        else:
            height = width / aspect_ratio
            print(height)

    # do we pass this in? this is confusing
    page_width, page_height = A4
    center_x = page_width / 2

    # Calculate the position to place the image to center it on the page
    x = center_x - (width / 2)

    canvas.drawImage(ImageReader(io.BytesIO(decoded_image_data)),
                     x, y - 130, width=width, height=height, mask='auto')
    # canvas.drawImage(ImageReader(image_reader), x, y - 130, width=width, height=height, mask='auto')
    logging.debug(
        f"Drawing image at x: {x}, y: {y-130} with width: {width}, height: {height}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <pdf_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, 'rb') as file:
        pdf_content = file.read()

    output_pdf = add_header_footer(file_path, pdf_content)
    # Save output_pdf to a file or process further...
    output_file_path = "modified_" + file_path.split('/')[-1]

    # Write the output PDF to a file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(output_pdf)

    print(f"Modified PDF saved as {output_file_path}")


if __name__ == "__main__":
    main()
