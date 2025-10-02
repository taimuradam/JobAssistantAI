from dataclasses import dataclass, field, asdict
from typing import List, Optional, Union, Dict
from enum import Enum
import json

class SectionType(str, Enum):
    education = "education"
    experience = "experience"
    projects = "projects"
    skills = "skills"
    certifications = "certifications"
    awards = "awards"
    publications = "publications"
    activities = "activities"
    volunteering = "volunteering"
    courses = "courses"
    other = "other"

@dataclass
class Contact:
    phones: List[str] = field(default_factory=list)
    emails: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)

@dataclass
class EducationItem:
    degree: Optional[str] = None
    field: Optional[str] = None
    school: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    currently_attending: Optional[bool] = None
    notes: Optional[str] = None
    coursework: Optional[List[str]] = None

@dataclass
class ExperienceItem:
    organization: Optional[str] = None
    title: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    current: Optional[bool] = None
    bullets: List[str] = field(default_factory=list)

@dataclass
class ProjectItem:
    name: Optional[str] = None
    date: Optional[str] = None
    bullets: List[str] = field(default_factory=list)
    technologies: Optional[List[str]] = None
    links: Optional[List[str]] = None

@dataclass
class SkillsItem:
    group: str = ""
    items: List[str] = field(default_factory=list)

@dataclass
class CertificationItem:
    name: str = ""
    issuer: Optional[str] = None
    issue_date: Optional[str] = None
    expiration_date: Optional[str] = None
    credential_id: Optional[str] = None
    url: Optional[str] = None

@dataclass
class GenericItem:
    label: Optional[str] = None
    value: Optional[str] = None
    bullets: Optional[List[str]] = None
    metadata: Optional[Dict[str, Union[str, int, float, bool]]] = None

Item = Union[EducationItem, ExperienceItem, ProjectItem, SkillsItem, CertificationItem, GenericItem]

@dataclass
class Section:
    type: SectionType
    title: str
    items: List[Item] = field(default_factory=list)

@dataclass
class Resume:
    id: Optional[str] = None
    name: str = ""
    contact: Contact = field(default_factory=Contact)
    summary: Optional[str] = None
    sections: List[Section] = field(default_factory=list)
    extra_sections: Dict[str, List[GenericItem]] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
