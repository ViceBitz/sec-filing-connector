from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from datetime import date


def validate_non_empty(v: str, field_name: str) -> str:
    if (not isinstance(v, str) or not v.strip()): #check string empty
        raise ValueError(field_name + " must be a non-empty string!")
    return v.strip()

class Company(BaseModel):
    """
    Company identity record
    """

    ticker: str
    cik: str
    name: str
    
    @field_validator("ticker")
    @classmethod
    #Validates ticker definition 
    def validate_ticker(cls, v: str) -> str:
        return validate_non_empty(v, "Ticker").upper()
    
    @field_validator("cik")
    @classmethod
    def validate_cik(cls, v: str) -> str:
        v = validate_non_empty(v, "CIK")
        if not v.isdigit():
            raise ValueError("CIK must contain only digits!")
        if len(v) > 10:
            raise ValueError("CIK must be at most 10 digits!")
        return v
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str):
        return validate_non_empty(v, "Name").upper()
    

class Filing(BaseModel):
    """
    Filing record
    """

    cik: str
    company_name: str
    form_type: str
    filing_date: date
    accession_number: str

    @field_validator("cik")
    @classmethod
    def validate_cik(cls, v: str) -> str:
        v = validate_non_empty(v, "CIK")
        if not v.isdigit():
            raise ValueError("CIK must contain only digits!")
        if len(v) > 10:
            raise ValueError("CIK must be at most 10 digits!")
        return v

    @field_validator("company_name")
    @classmethod
    def validate_name(cls, v: str):
        return validate_non_empty(v, "Company name").upper()

    @field_validator("form_type")
    @classmethod
    def validate_form_type(cls, v: str):
        return validate_non_empty(v, "Form type").upper()
    
    @field_validator("accession_number")
    @classmethod
    def validate_accession_number(cls, v: str):
        return validate_non_empty(v, "Accession number").upper()
    
class FilingFilter(BaseModel):
    form_types: list[str] | None = None
    date_from: date | None = None
    date_to: date | None = None
    limit: int = 10

    @field_validator("form_types")
    @classmethod
    def normalize_form_types(cls, v: list[str] | None) -> list[str] | None:
        if (v is None):
            return None
        if (not isinstance(v, list)):
            raise ValueError("Form types must be a list of strings!")
        
        cleaned = []
        for item in v:
            cleaned.append(validate_non_empty(item, "Form types").upper())
        return cleaned
    
    @field_validator("date_to")
    @classmethod
    def validate_date_range(cls, v: date | None, values) -> date | None:
        start = values.get("date_from")
        if start and v and start > v:
            raise ValueError("Date from cannot be after date to")
        return v