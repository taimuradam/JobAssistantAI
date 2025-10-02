#TO DO: Formatting has been completed
#NOW: Parse the PDF and seperate into dictionaries
#Send the dictionaries back through FASTAPI


#run it by going into the .venv: source .venv/bin/activate
#then do: uvicorn app.main:app --reload

from fastapi import FastAPI, UploadFile, File
from extractors import format_text, pdf, extract_text

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/resumes:parse")
async def parse_resume(file: UploadFile = File(...)):
    
    #collecting metadata
    data = await file.read()
    size = len(data)
    content_type = file.content_type
    name = file.filename
    extension = name.split(".")[-1].lower()

    #extracting raw text
    raw_text = filetype_call(extension, data)
    parsed_text = format_text.restructure(raw_text)
    name = extract_text.format(parsed_text)

    return {
        "filename": name,
        "extension": extension,
        "content_type": content_type,
        "size_bytes": size,
        "raw_text": raw_text,
        "parsed_text": parsed_text
    }

def filetype_call(extension: str, data: bytes):

    if extension == "pdf":
        return pdf.extract_pdf(data)
    else:
        return
