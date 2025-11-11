# SEC Connector Demo

A small testable module for looking up companies (ticker → CIK), listing their filings with filters, and printing results via a simple CLI.

---

## Installation

Create virtual environment and activate:
```
python3 -m venv venv
source venv/bin/activate
```

Install the package locally in editable mode:

```bash
pip install -e .
```

## Run Tests

Execute unit tests with pytest to validate models and client logic.

```bash
pytest tests/
```

Feel free to add more unit tests in test_client.py. This project uses AI-generated tests for convenience.

```python
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

```

## CLI Usage

CLI reads fixture data by default from tests/fixtures and can filter by form type, date range, and limit. You can also specify custom company / filings data files. Prints JSON to stdout for an easy check.

```bash
#All APPL filings
python3 -m sec_connector.cli AAPL

#10-K APPL filings, up to 5
python3 -m sec_connector.cli AAPL --form 10-K --limit 5

#APPL filings between 01/01/2024 and 12/13/2024
python3 -m sec_connector.cli AAPL --from_date 2024-01-01 --to_date 2024-12-31

#Specify alternate companies file
python3 -m sec_connector.cli AAPL --companies tests/fixtures/company_tickers2.json

#Specify alternate filings file
python3 -m sec_connector.cli AAPL --filings tests/fixtures/filings_sample2.json
```

## Other
- CIK values normalized to 10-digit zero-padded strings
- Form type filters are case-insensitive
- Date filters are inclusive, results sorted by newest
- Limit parameter caps returned filings after filtering
- Pydantic models check for valid company CIK, form types, dates

