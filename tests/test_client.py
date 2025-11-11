import json
from pathlib import Path
from datetime import date
import pytest

from sec_connector.client import SECClient
from sec_connector.models import FilingFilter, Company

"""
Some AI generated tests for the SEC filing connector
"""

# Fixture loader
def load_fixtures():
    path_filings = Path(__file__).parent / "fixtures/filings_sample.json"
    filings_data = json.loads(path_filings.read_text())
    path_companies = Path(__file__).parent / "fixtures/company_tickers.json"
    companies_data = json.loads(path_companies.read_text())
    return companies_data, filings_data


def test_lookup_company_valid():
    companies_data, _ = load_fixtures()
    client = SECClient(companies_data=companies_data)
    company = client.lookup_company("AAPL")
    assert isinstance(company, Company)
    assert company.ticker == "AAPL"
    assert company.cik == company.cik.zfill(10)


def test_lookup_company_invalid():
    companies_data, _ = load_fixtures()
    client = SECClient(companies_data=companies_data)
    with pytest.raises(ValueError):
        client.lookup_company("INVALID")


def test_list_filings_no_filters():
    companies_data, filings_data = load_fixtures()
    client = SECClient(companies_data=companies_data, filings_data=filings_data)
    filters = FilingFilter()
    results = client.list_filings("320193", filters)
    # Should return up to default limit
    assert len(results) <= filters.limit
    # Check descending sort
    dates = [f.filing_date for f in results]
    assert dates == sorted(dates, reverse=True)


def test_list_filings_form_type():
    companies_data, filings_data = load_fixtures()
    client = SECClient(companies_data=companies_data, filings_data=filings_data)
    filters = FilingFilter(form_types=["10-K"])
    results = client.list_filings("320193", filters)
    assert all(f.form_type.upper() == "10-K" for f in results)


def test_list_filings_date_range():
    companies_data, filings_data = load_fixtures()
    client = SECClient(companies_data=companies_data, filings_data=filings_data)
    filters = FilingFilter(date_from=date(2023, 1, 1), date_to=date(2023, 12, 31))
    results = client.list_filings("320193", filters)
    assert all(date(2023, 1, 1) <= f.filing_date <= date(2023, 12, 31) for f in results)


def test_list_filings_limit():
    companies_data, filings_data = load_fixtures()
    client = SECClient(companies_data=companies_data, filings_data=filings_data)
    filters = FilingFilter(limit=2)
    results = client.list_filings("320193", filters)
    assert len(results) <= 2


def test_list_filings_invalid_cik():
    companies_data, filings_data = load_fixtures()
    client = SECClient(companies_data=companies_data, filings_data=filings_data)
    filters = FilingFilter()
    assert not len(client.list_filings("", filters))


def test_filingfilter_invalid_dates():
    # Ensure date_from > date_to raises validation error
    with pytest.raises(ValueError):
        FilingFilter(date_from=date(2023, 12, 31), date_to=date(2023, 1, 1))