# Import the required modules
import sys
from PyPDF4 import PdfFileReader, PdfFileWriter, PdfFileMerger
from reportlab.pdfgen import canvas
import textwrap

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader 
# from reportlab.platypus import Frame, SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet

# import textwrap
import io
import base64
import os 

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

# TODO: NOTE: change to ALS 
footer_text_3 = """PSL Freight contracts a movement shall be treated as the responsible carrier in addition to the actual responsible carrier.
Registered Office: Liverpool Road, Eccles, Manchester, England, M30 7RF. Reg No. 2625304. VAT No. GB 570 4871 30
A MEMBER OF RHENUS LOGISTICS"""


# Get the current script's directory

als_header_dir = os.path.join(os.getcwd(), 'als_header')
# Define the font directory and file relative to the script's directory
font_dir = os.path.join(als_header_dir, '..', 'fonts')
font_file = "OpenSans-Regular.ttf"

# Create the font path and register the font
font_path = os.path.join(font_dir, font_file)
pdfmetrics.registerFont(TTFont("OpenSans", font_path))



from PyPDF4 import PdfFileMerger, PdfFileReader



def add_header_footer_to_pdf(file_name, input_file):
    # Create a PdfFileReader object to read the input file
    try:
        # reader = PdfReader(input_file)
        reader = PdfFileReader(io.BytesIO(input_file))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Create a PdfFileWriter object to write the output file
    writer = PdfFileWriter()

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

        # Create a canvas object to draw the footer and header
        canvas_obj = canvas.Canvas("temp.pdf", pagesize=A4)

        # Get the page width and height
        page_width, page_height = A4
        
        # Draw the footer text at the bottom center of the page
        canvas_obj.setFont("OpenSans", 8)
        # canvas_obj.drawCentredString(page_width / 2, 30, footer_text)

        # draw_image(canvas_obj, encoded_image_data, page_width / 2, page_height)

        # page_width and page_height are being passed in here
        draw_image(canvas_obj, encoded_image_data, page_width, page_height, 220, 180)


        draw_wrapped_line(canvas_obj, footer_text, 150, page_width / 2, 64, 10)
        draw_wrapped_line(canvas_obj, footer_text_2, 150, page_width / 2, 54, 10)
        draw_wrapped_line(canvas_obj, footer_text_3, 150, page_width / 2, 44, 10)
        
        # Save the canvas object
        canvas_obj.save()

        # Merge the canvas object with the current page
        watermark = PdfFileReader("temp.pdf")

        watermark_page = watermark.getPage(0)
        watermark_page.mergePage(page)
        writer.addPage(watermark_page)
        
        # remove temp.pdf
        os.remove("temp.pdf")

    # Create the output file name
    output_file_name = file_name + "_modified.pdf"
    file_path = f'{als_header_dir}\{output_file_name}'
    

    try:
        # create a temporary directory to write this to
        with open(file_path, "wb") as out:
            writer.write(out)

        if os.path.exists(file_path):
            print(f"File {output_file_name} created successfully at {file_path}")
        else:
            print(f"Error occurred while creating {output_file_name}")

        # now check if the file has been successfully created
        return output_file_name
        
    except Exception as e:
        # Print an error message if an exception occurs
        print(f"Error occurred while creating {output_file_name}: {str(e)}")
    
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
    
    # do we pass this in? this is confusing
    page_width, page_height = A4
    center_x = page_width / 2

    # Calculate the position to place the image to center it on the page
    x = center_x - (width / 2)
    
    canvas.drawImage(ImageReader(image_reader), x, y - 130, width=width, height=height, mask='auto')


# if __name__ == '__main__':
#     # Check if a pdf file is provided as an argument
    
#     if len(sys.argv) != 2:
#         print("Please provide a pdf file as an argument.")
#         sys.exit(1)

#     # Get the input pdf file name
#     input_file = sys.argv[1]


#     add_header_footer_to_pdf(input_file)
