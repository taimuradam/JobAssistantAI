from extractors import format_text
from data_structures import resume_schema as r
import spacy

nlp = spacy.load("en_core_web_sm")

def guess_name_spacy(extracted_text:list):
    lines = [ln for ln in extracted_text if isinstance(ln, str)]
    head = "\n".join(lines[:5])
    doc = nlp(head)
    cands = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]

    def ok(s:str):
        toks = s.split()
        if not (1 < len(toks) <= 4): return False
        if any(ch.isdigit() for ch in s): return False
        if "@" in s: return False
        return True
    
    for c in cands:
        if ok(c): 
            return c
    for ln in lines[:3]:
        if ok(ln): 
            return ln
    return None

def extract_name(extracted_text:list)->str:
    name = ""
    i = 0
    while i < len(extracted_text[0]):
        word = extracted_text[0][i]
        if not format_text.is_bullet_start(word):
            name += word
            i += 1
        else:
            return name
    return name

def extract_phone(extracted_text)->list:
    phones = []
    for line in extracted_text:
        matches = format_text.RE_PHONE.findall(line)
        phones.extend(matches)
    return phones

def extract_email(extracted_text:list)->list:
    emails = []
    for line in extracted_text:
        matches = format_text.RE_EMAIL.findall(line)
        emails.extend(matches)
    return emails

def extract_links(extracted_text: list) ->list:
    links = []
    for line in extracted_text:
        matches = format_text.RE_URL.findall(line)
        links.extend(matches)
    print (links)
    return links

def create_contact_item(extracted_text:list)->r.Contact:

    p = extract_phone(extracted_text)
    e = extract_email(extracted_text)
    l = extract_links(extracted_text)

    contact = r.Contact(
        phones=p,
        emails=e,
        links=l
    )

    return contact

def extract_summary(extracted_text:list)->str:
    i = 0
    while i < len(extracted_text):
        line = extracted_text[i]
        if line.upper() in format_text.SUMMARY_HEADERS:
            summary = extracted_text[i+1]
            print(summary)
            return summary
        i += 1
    return None

def create_resume_item(extracted_text:list)->r.Resume:
    s = guess_name_spacy(extracted_text) or extract_name(extracted_text)
    c = create_contact_item(extracted_text)
    sum = extract_summary(extracted_text)

    resume = r.Resume(
        name=s,
        contact=c,
        summary=sum
        )
    return resume

def format(extracted_text:list):

    resume = create_resume_item(extracted_text)
    print(resume.to_json())
    return