from extractors import format_text
from data_structures import resume_schema as r
import spacy, re, unicodedata

nlp = spacy.load("en_core_web_sm")

DEGREE_REGEX = format_text.DEGREE_REGEX
MAJOR_FALLBACK_RE = format_text.MAJOR_FALLBACK_RE
SUMMARY_HEADERS = format_text.SUMMARY_HEADERS
DELIMS_RE = format_text.DELIMS_RE
ORG_WORDS_RE = format_text.ORG_WORDS_RE
RE_PHONE = format_text.RE_PHONE
RE_URL = format_text.RE_URL
RE_EMAIL = format_text.RE_EMAIL
DELIMS_AFTER_MAJOR = format_text.DELIMS_AFTER_MAJOR
US_STATE_ABBR_TO_NAME = format_text.US_STATE_ABBR_TO_NAME
VALID_REGION_TOKENS = format_text.VALID_REGION_TOKENS
COUNTRY_ALIASES = format_text.COUNTRY_ALIASES
EDUCATION_HEADERS = format_text.EDUCATION_HEADERS
RE_HEADER_PREFIX = format_text.RE_HEADER_PREFIX
RE_DATE = format_text.RE_DATE

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
        matches = RE_PHONE.findall(line)
        phones.extend(matches)
    return phones

def extract_email(extracted_text:list)->list:
    emails = []
    for line in extracted_text:
        matches = RE_EMAIL.findall(line)
        emails.extend(matches)
    return emails

def extract_links(extracted_text: list) ->list:
    links = []
    for line in extracted_text:
        matches = RE_URL.findall(line)
        links.extend(matches)
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

def extract_summary(extracted_text:list)->str | None:
    i = 0
    while i < len(extracted_text):
        line = extracted_text[i]
        if line.upper() in SUMMARY_HEADERS:
            summary = extracted_text[i+1]
            return summary
        i += 1
    return None

def extract_degrees(extracted_text: list)->list:
    results = []
    for line in extracted_text:
        text = line.strip()
        m = DEGREE_REGEX.search(text)
        if m:
            degree = m.group(0)
            results.append(degree)

    return results

def _norm(s: str) -> str:
    return unicodedata.normalize("NFKC", s).strip()

def _clean_major(s: str) -> str:
    s = s.strip(" ,–—-:;")
    s = re.sub(r'^(?:in|of)\s+', '', s, flags=re.I).strip()
    return s

def _split_multi_majors(s: str) -> list[str]:
    parts = re.split(r'\s*(?:/|&|\+|,?\s+and\s+)\s+', s, flags=re.I)
    return [p.strip() for p in parts if p.strip()]

def extract_majors(extracted_text: list) -> list | None:
    out = []
    for raw in extracted_text:
        t = _norm(raw)
        m = DEGREE_REGEX.match(t)
        if not m:
            continue
        tail = t[m.end():].lstrip(" ,–—-:")
        m2 = MAJOR_FALLBACK_RE.search(tail)
        if m2:
            cand = (m2.group(1) or m2.group(2) or '').strip()
        else:
            cand = DELIMS_RE.split(tail, 1)[0].strip()
        if not cand:
            continue

        line_uniques = set()
        parts = []
        for p in _split_multi_majors(cand):
            pc = _clean_major(p)
            if pc and not ORG_WORDS_RE.search(pc) and pc not in line_uniques:
                line_uniques.add(pc)
                parts.append(pc)

        if not parts:
            chunks = [p.strip() for p in t[m.end():].split(",") if p.strip()]
            for p in chunks:
                pc = _clean_major(p)
                if pc and not ORG_WORDS_RE.search(pc) and pc not in line_uniques:
                    parts.append(pc)
                    break

        out.extend(parts)

    return out or None

def extract_schools(extracted_text: list) -> list | None:
    lines = [ln for ln in extracted_text if isinstance(ln, str) and ln.strip()]
    schools = []

    def ok(s: str) -> bool:
        if any(ch.isdigit() for ch in s): return False
        if "@" in s: return False
        if not ORG_WORDS_RE.search(s): return False
        toks = s.split()
        if not (1 < len(toks) <= 10): return False
        return True

    for doc in nlp.pipe(lines, batch_size=64):
        for ent in doc.ents:
            if ent.label_ != "ORG":
                continue
            c = ent.text.strip().strip(",;()[]{}")
            if not c:
                continue
            if ok(c):
                k = c.lower()
                schools.append(c)

    return schools or None

def _normalize_city_region(city: str, region: str) -> str:
    city = city.strip(" ,;()[]{}")
    region = region.strip(" ,;()[]{}")
    if region in US_STATE_ABBR_TO_NAME:
        region = US_STATE_ABBR_TO_NAME[region]
    if region in COUNTRY_ALIASES:
        region = COUNTRY_ALIASES[region]
    return f"{city}, {region}"

def _is_bad_token(s: str) -> bool:
    s = s.strip(" ,;()[]{}")
    if not s:
        return True
    if any(ch.isdigit() for ch in s) or "@" in s:
        return True
    return False

def _build_city_region_regex():
    region_alts = sorted(VALID_REGION_TOKENS, key=len, reverse=True)
    region_pat = "(?:" + "|".join(re.escape(x) for x in region_alts) + ")"
    return re.compile(rf"\b([A-Z][A-Za-z.\- ]{{1,40}}?),\s*({region_pat})\b(?!\s+[A-Za-z])")

CITY_REGION_REGEX = _build_city_region_regex()

def extract_locations(line: str) -> list | None:
    found = []
    line = line.strip()
    for m in CITY_REGION_REGEX.finditer(line):
        city, region = m.group(1), m.group(2)
        if _is_bad_token(city) or _is_bad_token(region):
            continue
        found.append(_normalize_city_region(city, region))

    return found or None

def extract_locations_education(extracted_text: list) -> list | None:
    in_edu = False
    out: list[str] = []

    for raw in extracted_text:
        line = raw.strip()
        if not line:
            if in_edu:
                loc = extract_locations(line)
                if loc != None:
                    out.append(loc) 
            continue

        m = RE_HEADER_PREFIX.match(line)
        if m:
            hdr = m.group('hdr').strip().upper()
            rest = m.group('rest').strip()

            if not in_edu:
                if hdr in EDUCATION_HEADERS:
                    in_edu = True
                    if rest:              # handle "Education: <content>" on same line
                        loc = extract_locations(line)
                        if loc != None:
                            out.append(loc) 
            else:
                break

            continue

        # Non-header line
        if in_edu:
            loc = extract_locations(line)
            if loc != None:
                out.append(loc) 
            
    return out or None

def _norm_present(s: str) -> str:
    return "Present" if s and s.strip().lower() == "present" else s.strip()

def extract_dates(line: str) -> list[str] | None:
    out: list[str] = []
    if line or not format_text.is_contact(line):
        for m in RE_DATE.finditer(line):
            start = m.group('start').strip()
            end = m.group('end')
            if end:
                out.append(f"{start} - {_norm_present(end)}")
            else:
                out.append(start)
    return out or None


def extract_education_dates(extracted_text: list):
    in_edu = False
    out: list[str] = []

    for raw in extracted_text:
        line = raw.strip()
        if not line:
            if in_edu:
                date = extract_dates(line)
                if date != None:
                    out.append(date) 
            continue

        m = RE_HEADER_PREFIX.match(line)
        if m:
            hdr = m.group('hdr').strip().upper()
            rest = m.group('rest').strip()

            if not in_edu:
                if hdr in EDUCATION_HEADERS:
                    in_edu = True
                    if rest:              # handle "Education: <content>" on same line
                        date = extract_dates(line)
                        if date != None:
                            out.append(date) 
            else:
                break

            continue

        # Non-header line
        if in_edu:
            date = extract_dates(line)
            if date != None:
                out.append(date) 
            
    return out or None

def extract_education():
    return

def create_education_item(extracted_text:list):

    degrees = extract_degrees(extracted_text)       #returns a list with all degrees
    print(degrees)
    majors = extract_majors(extracted_text)
    print(majors)
    schools = extract_schools(extracted_text)
    print(schools)
    locations = extract_locations_education(extracted_text)
    print(locations)
    dates = extract_education_dates(extracted_text)
    print(dates)

    return

def create_resume_item(extracted_text:list)->r.Resume:
    s = guess_name_spacy(extracted_text) or extract_name(extracted_text)
    c = create_contact_item(extracted_text)
    sum = extract_summary(extracted_text)

    global resume
    
    resume = r.Resume(
        name=s,
        contact=c,
        summary=sum
        )
    return resume

def format(extracted_text:list):

    resume = create_resume_item(extracted_text)
    print(resume.to_json())
    create_education_item(extracted_text)
    return