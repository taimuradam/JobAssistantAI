import pymupdf

def extract_pdf(data: bytes):
    file = pymupdf.open(stream=data, filetype="pdf")
    raw_text_list = []
    for page in file:
        page = page.get_text()
        raw_text_list.append(page)
    raw_text = "\n".join(raw_text_list)
    return raw_text