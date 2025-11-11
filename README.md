# SEC Connector Demo

A small testable module for looking up companies (ticker → CIK), listing their filings with filters, and printing results via a simple CLI.
---

## Installation

Install the package locally in editable mode for rapid iteration during development.

```bash
pip install -e .
```
## Run Tests

Execute unit tests with pytest to validate models and client logic.

```bash
pytest tests/
```

## CLI Usage

CLI reads fixture data by default from tests/fixtures and can filter by form type, date range, and limit. You can also specify custom company / filings data files. Prints JSON to stdout for an easy check.

```bash
#All APPL filings
python -m sec_connector.cli AAPL
#10-K APPL filings, up to 5
python -m sec_connector.cli AAPL --form 10-K --limit 5
#APPL filings between 01/01/2024 and 12/13/2024
python -m sec_connector.cli AAPL --from 2024-01-01 --to 2024-12-31
#Specify alternate companies file
python -m sec_connector.cli AAPL --companies tests/fixtures/company_tickers2.json
#Specify alternate filings file
python -m sec_connector.cli AAPL --filings tests/fixtures/filings_sample2.json
```

## Other
- CIK values normalized to 10-digit zero-padded strings
- Form type filters are case-insensitive
- Date filters are inclusive, results sorted by newest
- Limit parameter caps returned filings after filtering
- Pydantic models check for valid company CIK, form types, dates

