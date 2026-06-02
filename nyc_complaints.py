import argparse
import requests
from datetime import datetime, timedelta

API_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

BOROUGHS = {
    "BRONX",
    "BROOKLYN",
    "MANHATTAN",
    "QUEENS",
    "STATEN ISLAND",
}

def int_between(min_value=None, max_value=None):
    def checker(value):
        try:
            value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError("must be an integer")

        if min_value is not None and value < min_value:
            raise argparse.ArgumentTypeError(f"must be at least {min_value}")

        if max_value is not None and value > max_value:
            raise argparse.ArgumentTypeError(f"must be at most {max_value}")

        return value
    return checker

def validate_zip_code(value):
    if not value.isdigit() or len(value) != 5:
        raise argparse.ArgumentTypeError("must be a 5-digit ZIP code")
    return value

def validate_borough(value):
    borough = value.strip().upper()
    if borough not in BOROUGHS:
        raise argparse.ArgumentTypeError(f"must be one of: {', '.join(BOROUGHS)}")
    return borough

def parse_args():
    parser = argparse.ArgumentParser(
        description="Summarize recent NYC 311 complaints."
    )

    location_group = parser.add_mutually_exclusive_group()

    location_group.add_argument(
        "--borough",
         default=None,
         type=validate_borough,
         help="Only include complaints from this borough."
    )

    location_group.add_argument(
        "--zip",
        dest="zip_code",
        default=None,
        type=validate_zip_code,
        help="Only include complaints from this ZIP code."
    )

    parser.add_argument(
        "--days",
        type=int_between(2, 365),
        default=7,
        help="Number of recent days to query. Default: 7. Must be between 2 and 365."
    )

    parser.add_argument(
        "--top",
        type=int_between(1, None),
        default=None,
        help="Maximum number of complaint types to show. If omitted, show all."
    )

    parser.add_argument(
        "--min-count",
        type=int_between(1, None),
        default=1,
        help="Only show complaint types with at least this many reports. Default: 1."
    )

    return parser.parse_args()

def create_params(args):
    borough = args.borough
    zip_code = args.zip_code
    days = args.days
    top = args.top
    mincount = args.min_count
    start_date = datetime.now() - timedelta(days=days)
    start_date_string = start_date.strftime("%Y-%m-%dT%H:%M:%S")
    where = f"created_date >= '{start_date_string}'"
    if borough is not None:
        where += f" AND borough = '{borough}'"
    if zip_code is not None:
        where += f" AND incident_zip = '{zip_code}'"

    params = {
        "$select": "complaint_type, count(*) AS count",
        "$where": where,
        "$group": f"complaint_type HAVING count >= {mincount}",
        "$order": "count DESC",
    }
    if top is not None:
        params["$limit"] = top
    return params

def fetch_complaints(params):
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error fetching data: {error}")
        return []

def pretty_print(args, data):
    if len(data) == 0:
        return
    else:
        if args.borough:
            location = args.borough.title()
        elif args.zip_code:
            location = args.zip_code
        else:
            location = "NYC"
        print(f"Top 311 complaints in {location} over the last {args.days} days\n")
        for i, complaint in enumerate(data, start=1):
            print(f"{i}. {complaint['complaint_type']}: {complaint['count']}" )

def main():
    args = parse_args()
    params = create_params(args)
    data = fetch_complaints(params)
    pretty_print(args, data)
    
if __name__ == "__main__":
    main()
