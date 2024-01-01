import io
import logging
from PyPDF2 import PdfReader, PdfWriter


def resave_pdf(file_name, input_file):
    logging.info("Starting to resave the file")
    try:
        reader = PdfReader(io.BytesIO(input_file))
        writer = PdfWriter()

        # Iterate through each page and add it to the writer
        for page in reader.pages:
            writer.add_page(page)

        # Write the modified content to an in-memory binary stream
        output_stream = io.BytesIO()
        writer.write(output_stream)
        output_stream.seek(0)

        # Check if resaving was successful
        if len(reader.pages) == len(PdfReader(output_stream).pages):
            logging.info("PDF resaving successful")
            return output_stream.getvalue()
        else:
            logging.error("PDF resaving failed: Page count mismatch")
            return None
    except Exception as e:
        logging.error(f"Error processing PDF file: {e}")
        return None
