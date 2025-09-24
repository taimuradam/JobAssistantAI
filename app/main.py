#TO DO: First thing is finish parse() in parse_text by seperating
#The raw text has been cleaned, now you need to make the dictionary format and send it back through FastAPI
#After that, do the same thing for docx files

#run it by going into the .venv: source .venv/bin/activate
#then do: uvicorn app.main:app --reload

from fastapi import FastAPI, UploadFile, File
from extractors import pdf, docx, parse_text

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

    parsed_text = parse_text.parse(raw_text)

    return {
        "filename": name,
        "extension": extension,
        "content_type": content_type,
        "size_bytes": size,
        "raw_text": raw_text
    }

def filetype_call(extension: str, data: bytes):

    if extension == "pdf":
        return pdf.extract_pdf(data)
    elif extension == "docx":
        return
    else:
        return
