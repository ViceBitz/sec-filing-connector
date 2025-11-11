from .models import Company, Filing, FilingFilter
from typing import Iterable

class SECClient:
    def __init__(self, companies_data: dict[str, dict], filings_data: Iterable[dict] = None):
        self.companies: dict[str, Company] = {}
        for ticker, info in companies_data.items(): #Build company models
            try:
                company = Company(
                    ticker=ticker,
                    cik=str(info["cik"]).zfill(10),
                    name=str(info["name"])
                )
            except Exception as e: #actually throw error when model invalid
                raise ValueError(f"Invalid company data for {ticker} : {e}")
            
            self.companies[company.ticker] = company
        
        self.filings: list[Filing] = []

        if filings_data:
            for f in filings_data: #Build filing models
                try:
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
                except Exception as e: #actually throw error when model invalid
                    raise ValueError(f"Invalid filing data for {cik} : {e}")
    """
    - Normalize ticker to upper-case
    - Fill CIK to 10 digits
    - Check ticker -> company
    - Create Company obj
    """
    #Normalize ticker to upper-case, fill cik to 10 digits, create Company obj
    def lookup_company(self, ticker: str) -> Company:
        t_norm = ticker.strip().upper()
        company = self.companies.get(t_norm)
        if not company:
            raise ValueError(f"Company not found for ticker '{t_norm}'")
        cik = str(company.cik).zfill(10)
        return company


    """
    - Fill CIK to 10 digits
    - Filter form types and date ranges
    *Note: does not check for invalid cik, per instructions
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