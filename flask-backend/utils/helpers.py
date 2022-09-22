import fitz

# TODO: 

class Helpers:
    def __init__(self, path_to_pdf):
        self.pdf = path_to_pdf

    def load_pdf(path_to_pdf):
        doc = fitz.open(path_to_pdf)
        return doc

    def convert_all_pages_to_pdf(path_to_pdf):
        doc = fitz.open(path_to_pdf)
        
        full_text = ""
        for page in doc:
            text = page.get_text("text")
            full_text += text
        
        return full_text
    
    # print(full_text)
    # print(full_text.split('\n'))
    # doc.close()
    