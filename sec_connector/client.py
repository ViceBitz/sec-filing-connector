from .models import Company, Filing, FilingFilter
from typing import Iterable

class SECClient:
    def __init__(self, companies_data: dict[str, dict], filings_data: Iterable[dict] = None):
        self.companies = companies_data
        self.filings: list[Filing] = []

        if filings_data:
            for f in filings_data:
                cik = str(f["cik"])
                self.filings.append(
                    Filing(
                        cik=cik,
                        company_name=f["company_name"],
                        form_type=f["form_type"],
                        filing_date=f["filing_date"],
                        accession_number=f["accession_number"]
                    )
                )

    """
    - Normalize ticker to upper-case
    - Fill CIK to 10 digits
    - Check ticker -> company
    - Create Company obj
    """
    #Normalize ticker to upper-case, fill cik to 10 digits, create Company obj
    def lookup_company(self, ticker: str) -> Company:
        t_norm = ticker.strip().upper()
        info = self.companies.get(t_norm)
        if not info:
            raise ValueError(f"Company not found for ticker '{t_norm}'")
        cik = str(info["cik"]).zfill(10)
        return Company(ticker=t_norm, cik=cik, name=str(info["name"]))


    """
    - Fill CIK to 10 digits
    - Filter form types and date ranges
    """
    def list_filings(self, cik: str, filters: FilingFilter) -> list[Filing]:
        cik_norm = str(cik).zfill(10)
        results = [f for f in self.filings if f.cik == cik_norm]

        if filters.form_types: #filter form type
            ft_set = {ft.upper() for ft in filters.form_types}
            results = [f for f in results if f.form_type.upper() in ft_set]

        if filters.date_from: #date range filter
            results = [f for f in results if f.filing_date >= filters.date_from]
        if filters.date_to:
            results = [f for f in results if f.filing_date <= filters.date_to]
        
        results.sort(key=lambda f: f.filing_date, reverse=True) #sort by latest date
        return results[: filters.limit] #limit file count