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

def parse_args():
    parser = argparse.ArgumentParser(
        description="Summarize recent NYC 311 complaints."
    )

    parser.add_argument(
        "--borough",
         default=None,
         choices=BOROUGHS,
         help="Only include complaints from this borough."
    )

    parser.add_argument(
        "--days",
        type=int_between(2, 365),
        default=7,
        help="Number of recent days to query. Default: 7. Must be between 2 and 365,"
    )

    parser.add_argument(
        "--top",
        type=int_between(1, None),
        default=None,
        help="Maximum number of complaint types to show. If ommitted, show all."
    )

    parser.add_argument(
        "--min-count",
        type=int,
        default=0,
        help="Only show complaint types with at least this many reports."
    )

    return parser.parse_args()

def create_params(args):
    borough = args.borough
    days = args.days
    top = args.top
    mincount = args.min_count
    start_date = datetime.now() - timedelta(days=days)
    start_date_string = start_date.strftime("%Y-%m-%dT%H:%M:%S")
    where = f"created_date >= '{start_date_string}'"
    if borough is not None:
        where += f" AND borough = '{borough}'"
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
    response = requests.get(API_URL, params=params)
    data = response.json()
    return data

def pretty_print(days, data):
    for i, complaint in enumerate(data, start=1):
        print(f"{i}. {complaint['complaint_type']}: {complaint['count']}" )

def main():
    args = parse_args()
    params = create_params(args)
    data = fetch_complaints(params)
    days = args.days
    pretty_print(days, data)
    
if __name__ == "__main__":
    main()
