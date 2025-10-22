import re

MONTHS = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*'
RE_EMAIL = re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', re.I)
RE_PHONE = re.compile(r'\b(?:\+?\d[\d\-\s().]{7,}\d)\b')
RE_URL = re.compile(
    r'(https?://[^\s•]+|www\.[^\s•]+|linkedin\.com/[^\s•]+|github\.com/[^\s•]+)',
    re.I
)
RE_BULLET = re.compile(r'^(\s*)(->|•|-|\*|—|·|○|▪|▸)\s+')

SUMMARY_HEADERS = {
    "SUMMARY", "PROFESSIONAL SUMMARY", "CAREER SUMMARY",
    "PROFILE", "PROFESSIONAL PROFILE", "OBJECTIVE", "ABOUT ME"
}

EDUCATION_HEADERS = {
    "EDUCATION", "EDUCATIONAL BACKGROUND", "ACADEMICS",
    "ACADEMIC BACKGROUND", "ACADEMIC HISTORY", "EDUCATIONAL HISTORY",
    "ACADEMIC QUALIFICATIONS", "QUALIFICATIONS", "SCHOLASTIC RECORD",
    "TRAINING & EDUCATION", "SCHOOLING"
}

HEADERS = SUMMARY_HEADERS | EDUCATION_HEADERS | {
    "SUMMARY", "EDUCATION", "EXPERIENCE", "PROJECTS", "SKILLS",
    "CERTIFICATIONS", "AWARDS", "PUBLICATIONS", "LEADERSHIP",
    "PROFESSIONAL EXPERIENCE", "TECHNICAL SKILLS",
}

RE_HEADER_WORDS = re.compile(
    r'^(?:' + '|'.join(map(re.escape, HEADERS)) + r')\s*:?\s*$',
    re.I
)

RE_DATE = re.compile(
    rf'(?P<start>(?:{MONTHS}\.?\s+\d{{4}}|\b\d{{4}}\b))'
    rf'(?:\s*(?:–|-|to)\s*(?P<end>Present|{MONTHS}\.?\s+\d{{4}}|\d{{4}}))?',
    re.I
)

RE_ROLE_ORG = re.compile(r'^[^-:]+,\s*[A-Za-z .]+(?:,?\s*[A-Z]{2})?:\s*[^-]+$')
RE_ALLCAPS = re.compile(r'^[A-Z0-9 &/]+$')
RE_COLON = re.compile(r'[:\uFF1A]')

DEGREE_REGEX = re.compile(
    r'^\s*(?:[•\-\u2022–—]\s*)?(?:'
    r'(?:B\.?\s?S\.?|B\.?\s?A\.?|B\.?\s?Sc\.?|BEng|B\.?\s?Eng\.?|BE|BCom|B\.?\s?Com\.?|BBA|BFA|B\.?\s?F\.?\s?A\.?|BEd|B\.?\s?Ed\.?)'
    r'|(?:M\.?\s?S\.?|M\.?\s?A\.?|M\.?\s?Sc\.?|MEng|M\.?\s?Eng\.?|ME|MBA|MEd|M\.?\s?Ed\.?|MPH|MPP|MPS|MSCS)'
    r'|(?:Ph\.?\s?D\.?|PhD|DPhil|Ed\.?\s?D\.?|EdD|Sc\.?\s?D\.?|DSc)'
    r'|(?:Associate of (?:Arts|Science))'
    r'|(?:Bachelor of (?:Arts|Science|Engineering|Commerce|Education|Fine Arts|Business Administration))'
    r'|(?:Master of (?:Arts|Science|Engineering|Education|Business Administration|Public Health|Public Policy|Professional Studies))'
    r'|(?:Doctor of (?:Philosophy|Education|Science))'
    r'|(?:Certificate(?:\s+in)?)'
    r'|(?:Minor(?:\s+in)?)'
    r'|(?:Concentration(?:\s+in)?)'
    r'|(?:Diploma(?:\s+in)?)'
    r')(?=,|:|\s|$)',
    re.I
)

MAJOR_FALLBACK_RE = re.compile(
    r'(?:\b(?:in|of|:)\s+([A-Za-z0-9&/\-\.\s]+?)(?=(?:,|;|•|\(|\)|\bat\b|\bfrom\b|–|—|-|$)))'
    r'|(?:,\s*([A-Za-z0-9&/\-\.\s]+?)(?=(?:,|;|•|\(|\)|\bat\b|\bfrom\b|–|—|-|$)))',
    re.I
)

ORG_WORDS_RE = re.compile(r'\b(University|College|Institute|School|Academy|Polytechnic|Faculty|Department)\b', re.I)
DELIMS_RE = re.compile(r'\s*(?:,|\bat\b|\bfrom\b|–|—|-|\(|;|:|$)\s*', re.I)
DELIMS_AFTER_MAJOR = re.compile(r'\s*(?:,|;|•|\(|\)|–|—|-|\bat\b|\bfrom\b|:)\s*', re.I)

MONTH_YEAR_RE = re.compile(r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}\b|\b20\d{2}\b', re.I)
CERT_MINOR_RE = re.compile(r'\b(?:Certificate|Minor|Concentration|Honou?rs?|Track|Speciali[sz]ation|Emphasis)\b', re.I)
DELIM_RE = re.compile(r'\s*(?:[,;•()–—-]|\bat\b|\bfrom\b)\s*', re.I)

ABBREV_END = re.compile(
    r'(?:\b(?:Inc|LLC|Ltd|Co|Corp|Sr|Jr|St|Rd|Ave|Blvd|Dr|Ms|Mr|Mrs|U\.S|U\.K|B\.S|M\.S|Ph\.D|M\.A|B\.A|MEng|BEng)\.)$',
    re.I
)

US_STATE_ABBR_TO_NAME = {
    "AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado",
    "CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho",
    "IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana",
    "ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi",
    "MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey",
    "NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio",
    "OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina",
    "SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia",
    "WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming","DC":"District of Columbia"
}

COUNTRY_ALIASES = {
    "US":"United States", "U.S.":"United States", "USA":"United States",
    "UK":"United Kingdom", "UAE":"UAE"
}

US_STATE_NAMES = set(US_STATE_ABBR_TO_NAME.values())
VALID_REGION_TOKENS = set(US_STATE_ABBR_TO_NAME.keys()) | US_STATE_NAMES | {
    "United States","United Kingdom","UAE","Pakistan","Canada","Mexico","USA","US","U.S.","UK"
}

RE_HEADER_PREFIX = re.compile(
    r'^\s*(?P<hdr>' + '|'.join(map(re.escape, HEADERS)) + r')\s*:?\s*(?P<rest>.*)$',
    re.I
)

def is_block_boundary(line: str) -> bool:
    t = line.strip()
    if not t: return True
    if is_header(t) or is_contact(t) or is_bullet_start(t) or is_date(t) or is_role(t):
        return True
    if RE_COLON.search(t) and (RE_HEADER_WORDS.match(t) or t.endswith(':')):
        return True
    if DEGREE_REGEX.search(t):
        return True
    return False

def should_join(l1: str, l2: str) -> bool:
    a = l1.strip()
    b = l2.strip()
    if not a or not b: return False
    if is_block_boundary(a) or is_block_boundary(b): return False
    if RE_DATE.fullmatch(b): return False
    if a.endswith('-'): return True
    if ABBREV_END.search(a): return True
    return True

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
            nxt = merged_lines[j].lstrip()
            if cur.endswith('-'):
                cur = cur[:-1] + nxt
            else:
                cur = cur + " " + nxt
            j += 1
        single_lines.append(cur)
        i = j

    return single_lines