import argparse
import json
from datetime import datetime
from pathlib import Path
from sec_connector.client import SECClient
from sec_connector.models import FilingFilter

def main():
    parser = argparse.ArgumentParser(description="Simple SEC filings CLI")
    parser.add_argument("ticker", type=str, help="Company ticker")
    parser.add_argument("--form", type=str, nargs="*", help="Form types to filter (e.g. 10-K 10-Q)")
    parser.add_argument("--limit", type=int, default=10, help="Max number of filings")
    parser.add_argument("--data-file", type=str, default=None, help="Optional JSON file with test filings")
    args = parser.parse_args()

    #Example companies data
    companies_data = {
        "AAPL": {"cik": "320193", "name": "Apple Inc."},
        "TSLA": {"cik": "1318605", "name": "Tesla Inc."},
    }

    #Load filingsg
    filings_data = []
    if args.data_file:
        path = Path(args.data_file)
        if path.exists():
            filings_data = json.loads(path.read_text())

    client = SECClient(companies_data=companies_data, filings_data=filings_data)
    filters = FilingFilter(form_types=args.form, limit=args.limit)

    #Lookup companies and filings
    company = client.lookup_company(args.ticker)
    filings = client.list_filings(company.cik, filters)

    #Format to JSON
    output = [
        {
            "cik": f.cik,
            "company_name": f.company_name,
            "form_type": f.form_type,
            "filing_date": f.filing_date.isoformat(),
            "accession_number": f.accession_number,
        }
        for f in filings
    ]

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
