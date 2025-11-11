from pydantic import BaseModel, Field, field_validator
from datetime import date
from __future__ import annotations


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
        if (not isinstance(v, str) or not v.strip()): #check string empty
            raise ValueError("Ticker must be non-empty!")
        return v.strip()
    
    @field_validator("cik")
    @classmethod
    def validate_cik(cls, v: str) -> str:
        if (not isinstance(v, str) or not v.strip()): #check string empty
            raise ValueError("cik must be non-empty!")
        v = v.strip()

        #Make sure cik only has digits and up to 10
        if (not v.isdigit()):
            raise ValueError("cik must contain only digits!")
        if (len(v) > 10):
            raise ValueError("cik must be at most 10 digits!")
        return v
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str):
        if (not isinstance(v, str) or not v.strip()): #check string empty
            raise ValueError("Name must be non-empty!")
        return v.strip()
    

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
        if (not isinstance(v, str) or not v.strip()): #check string empty
            raise ValueError("cik must be non-empty!")
        v = v.strip()

        #Make sure cik only has digits and up to 10
        if (not v.isdigit()):
            raise ValueError("cik must contain only digits!")
        if (len(v) > 10):
            raise ValueError("cik must be at most 10 digits!")
        return v

    @field_validator("company_name")
    @classmethod
    def validate_name(cls, v: str):
        if (not isinstance(v, str) or not v.strip()): #check string empty
            raise ValueError("Name must be non-empty!")
        return v.strip()

    @field_validator("form_type")
    @classmethod
    def validate_form_type(cls, v: str):
        if (not isinstance(v, str) or not v.strip()): #check string empty
            raise ValueError("Form type must be non-empty!")
        return v.strip()
    
    @field_validator("accession_number")
    @classmethod
    def validate_form_type(cls, v: str):
        if (not isinstance(v, str) or not v.strip()): #check string empty
            raise ValueError("Accession number must be non-empty!")
        return v.strip()
    
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
            if not isinstance(item, str) or not item.strip(): #check non-empty
                raise ValueError("Form types must be non-empty!")
            cleaned.append(item.strip().upper())
        return cleaned
    
    @field_validator("date_to")
    @classmethod
    def validate_date_range(cls, v: date | None, values) -> date | None:
        start = values.get("date_from")
        if start and v and start > v:
            raise ValueError("Date from cannot be after date to")
        return v