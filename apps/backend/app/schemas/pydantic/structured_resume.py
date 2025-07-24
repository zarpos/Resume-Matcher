from typing import List, Optional
from pydantic import BaseModel, Field


class Location(BaseModel):
    city: Optional[str] = "Unknown City"
    country: Optional[str] = "Unknown Country"


class PersonalData(BaseModel):
    firstName: str = Field(..., alias="firstName")
    lastName: Optional[str] = Field(..., alias="lastName")
    email: str
    phone: str
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None
    location: Location


class Experience(BaseModel):
    job_title: Optional[str] = Field("Unknown Position", alias="jobTitle")
    company: Optional[str] = "Unknown Company"
    location: Optional[str] = "Unknown Location"
    start_date: Optional[str] = Field("Unknown", alias="startDate")
    end_date: Optional[str] = Field("Unknown", alias="endDate")
    description: List[str] = Field(default_factory=list)
    technologies_used: Optional[List[str]] = Field(
        default_factory=list, alias="technologiesUsed"
    )


class Project(BaseModel):
    project_name: Optional[str] = Field("Unknown Project", alias="projectName")
    description: Optional[str] = "Unknown Description"
    technologies_used: List[str] = Field(default_factory=list, alias="technologiesUsed")
    link: Optional[str] = None
    start_date: Optional[str] = Field(None, alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")


class Skill(BaseModel):
    category: Optional[str] = "General"
    skill_name: Optional[str] = Field("Unknown Skill", alias="skillName")


class ResearchWork(BaseModel):
    title: Optional[str] = None
    publication: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None


class Education(BaseModel):
    institution: Optional[str] = "Unknown Institution"
    degree: Optional[str] = "Unknown Degree"
    field_of_study: Optional[str] = Field(None, alias="fieldOfStudy")
    start_date: Optional[str] = Field("Unknown", alias="startDate")
    end_date: Optional[str] = Field("Unknown", alias="endDate")
    grade: Optional[str] = None
    description: Optional[str] = None


class StructuredResumeModel(BaseModel):
    personal_data: PersonalData = Field(..., alias="Personal Data")
    experiences: List[Experience] = Field(..., alias="Experiences")
    projects: List[Project] = Field(..., alias="Projects")
    skills: List[Skill] = Field(..., alias="Skills")
    research_work: List[ResearchWork] = Field(
        default_factory=list, alias="Research Work"
    )
    achievements: List[str] = Field(default_factory=list, alias="Achievements")
    education: List[Education] = Field(..., alias="Education")
    extracted_keywords: List[str] = Field(
        default_factory=list, alias="Extracted Keywords"
    )

    class ConfigDict:
        validate_by_name = True
        str_strip_whitespace = True
