from pdf2image import convert_from_path
import sys

# command line interface
# use argv to get the path from command line
def get_file_path():
    return sys.argv[1]

# output to specific folder

# TODO: play with sizes of conversions - dpi, output size
# balance speed with accuracy. Accuracy is more important
def convert_pdf_to_image(path_to_pdf):
    # windows 
    pages = convert_from_path(path_to_pdf, size=2000, dpi=300, poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
    return pages

# FIXME: edit this for any input
def output_to_folder(pages):
    for i, page in enumerate(pages):
        page.save(f'./tmp/output-{i}.jpg', 'JPEG')

def main():
    path_to_pdf = get_file_path()
    pages = convert_pdf_to_image(path_to_pdf)
    output_to_folder(pages)

if __name__ == "__main__":
    main()