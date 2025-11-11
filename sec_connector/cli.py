import argparse
import json
from datetime import datetime
from pathlib import Path
from sec_connector.client import SECClient
from sec_connector.models import FilingFilter

#Convert YYYY-MM-DD to datetime.data
def parse_date(date_str: str | None):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")
    
def main():
    parser = argparse.ArgumentParser(description="Simple SEC filings CLI")
    parser.add_argument("ticker", type=str, help="Company ticker")
    parser.add_argument("--form", type=str, nargs="*", default=None, help="Form types to filter (e.g. 10-K 10-Q)")
    parser.add_argument("--from", type=str, default=None, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--to", type=str, default=None, help="End date (YYYY-MM-DD)")
    parser.add_argument("--limit", type=int, default=10, help="Max number of filings")
    parser.add_argument("--companies", type=str, default="tests/fixtures/company_tickers.json",
                        help="Path to company tickers JSON")
    parser.add_argument("--filings", type=str, default="tests/fixtures/filings_sample.json",
                        help="Path to filings JSON")
    
    args = parser.parse_args()

    #read from test files
    companies_path = Path(args.companies)
    filings_path = Path(args.filings)
    companies_data = json.loads(companies_path.read_text())
    filings_data = json.loads(filings_path.read_text())

    #make client
    client = SECClient(companies_data=companies_data, filings_data=filings_data)
    try:
        company = client.lookup_company(args.ticker)
    except ValueError as e:
        print(f"Error: {e}")
        return

    date_from = parse_date(args.date_from)
    date_to = parse_date(args.date_to)

    #make filters
    filters = FilingFilter(
        form_types=[f.upper() for f in args.form] if args.form else None,
        date_from=date_from,
        date_to=date_to,
        limit=args.limit
    )
    results = client.list_filings(company.cik, filters)

    if not results:
        print(f"No filings found for {company.ticker} with given filters")
        return

    #output as json
    output = [f.model_dump() for f in results]
    print(json.dumps(output, indent=2, sort_keys=True, default=str))

if __name__ == "__main__":
    main()
