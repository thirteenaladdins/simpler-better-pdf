import fitz


def load_pdf(path_to_pdf):
    doc = fitz.open(path_to_pdf)
    
    full_text = ""
    for page in doc:
        text = page.get_text("text")
        full_text += text
    
    # print(full_text)
    # print(full_text.split('\n'))
    # doc.close()
    return full_text