import re

MONTHS = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*'
RE_EMAIL = re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', re.I)
RE_PHONE = re.compile(r'\b(?:\+?\d[\d\-\s().]{7,}\d)\b')
RE_URL = re.compile(r'(https?://\S+|www\.\S+|linkedin\.com/\S+|github\.com/\S+)', re.I)
RE_BULLET = re.compile(r'^(\s*)(->|•|-|\*|—|·|○|▪|▸)\s+')
import re

HEADERS = [
    "SUMMARY", "EDUCATION", "EXPERIENCE", "PROJECTS", "SKILLS",
    "CERTIFICATIONS", "AWARDS", "PUBLICATIONS", "LEADERSHIP",
    "PROFESSIONAL EXPERIENCE", "TECHNICAL SKILLS",
]

RE_HEADER_WORDS = re.compile(
    r'^(?:' + '|'.join(map(re.escape, HEADERS)) + r')\s*:?\s*$',
    re.I
)

RE_DATE = re.compile(
    rf'({MONTHS}\.?\s+\d{{4}}|\b\d{{4}}\b)(?:\s*(?:–|-|to)\s*(Present|{MONTHS}\.?\s+\d{{4}}|\d{{4}}))?',
    re.I
)
RE_ROLE_ORG = re.compile(r'^[^-:]+,\s*[A-Za-z .]+(?:,?\s*[A-Z]{2})?:\s*[^-]+$')
RE_ALLCAPS = re.compile(r'^[A-Z0-9 &/]+$')
RE_COLON = re.compile(r'[:\uFF1A]')

def should_join(l1:str, l2:str)->bool:
    if (not is_header(l1) and not is_contact(l1) and not is_date(l1)):
        if (not is_header(l2) and not is_contact(l2) and not is_date(l2) and not is_colon(l2)):
            return True
    return False

def is_header(line: str) -> bool:
    l = line.strip()
    if RE_HEADER_WORDS.match(l): return True
    if 2 <= len(l) <= 60 and RE_ALLCAPS.match(l):
        letters = [c for c in l if c.isalpha()]
        if letters and sum(c.isupper() for c in letters) / len(letters) >= 0.7:
            return True
    return False

def starts_like_new_block(s: str) -> bool:
    t = s.strip()
    if not t: return True
    if is_header(t) or is_contact(t) or is_bullet_start(t) or is_date(t) or is_role(t):
        return True
    # ALLCAPS token followed by colon
    if re.match(r'^[A-Z][A-Z &/]{2,}:$', t): return True
    return False
    
def is_contact(line:str)->bool:
    return (RE_EMAIL.search(line) or RE_URL.search(line) or RE_PHONE.search(line))
    
def is_bullet_start(line:str)->bool:
    return bool(RE_BULLET.match(line))
    
def is_date(line:str)->bool:
    return bool(RE_DATE.search(line))

def is_role(line:str)->bool:
    return bool(RE_ROLE_ORG.match(line.strip()))

def is_colon(line:str)->bool:
    return bool(RE_COLON.search(line))

def restructure(raw_text:str):

    #remove newlines and weird spacing characters
    cleaned_text = raw_text.replace("\u200b", "")
    lines = cleaned_text.split("\n")

    #remove all empty lines
    non_empty_lines = [line.strip() for line in lines if line.strip()]

    merged_lines = []
    i = 0

    #if -> comes first and then there is a new line with the bullets, put it on one line
    #For example if the structure of it is:
    #->
    #Enhanced semantic keyword mapping and automated section scoring using NLP pipelines
    #Then it will convert point to be:
    #-> Enhanced semantic keyword mapping and automated section scoring using NLP pipelines
    while i < len(non_empty_lines):
        cur = non_empty_lines[i].strip()
        if is_bullet_start(cur):
            if i+1 < len(non_empty_lines):
                next_line = non_empty_lines[i+1].lstrip()
                cur += " " + next_line
                merged_lines.append(cur)
                i += 2
            else:
                merged_lines.append(cur)
                i += 1
        else:
            merged_lines.append(cur)
            i += 1

    #Since the PDF gets parsed into multiple lines per paragraph, this algorithm combines all lines into one paragraph
    single_lines = []
    i = 0
    while i < len(merged_lines):
        cur = merged_lines[i].strip()
        j = i + 1
        while j < len(merged_lines) and should_join(cur, merged_lines[j]):
            cur += " " + merged_lines[j]
            j = j+1
        single_lines.append(cur)
        i = j

    for line in single_lines:
        print(line)

    return single_lines