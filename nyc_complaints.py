import argparse
import requests
from datetime import datetime, timedelta

url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--borough", required=True)
    return parser.parse_args()

def fetch_complaints(borough):
    days = 30
    start_date = datetime.now() - timedelta(days=days)
    start_date_string = start_date.strftime("%Y-%m-%dT%H:%M:%S")
    response = requests.get(url, params={
        "$select": "complaint_type, count(*) AS count",
        "$where": f"borough = '{borough}' AND created_date >= '{start_date_string}'",
        "$group": "complaint_type",
        "$order": "count DESC",
        "$limit": 10
    })
    data = response.json()
    return data

def pretty_print(borough, data):
    print(f"Top 10 Complaints for  {borough} over last 30 days")
    for i, complaint in enumerate(data, start=1):
        print(f"{i}. {complaint['complaint_type']}: {complaint['count']}" )

def main():
    args = parse_args()
    borough = args.borough
    data = fetch_complaints(borough)
    pretty_print(borough, data)
    
if __name__ == "__main__":
    main()
