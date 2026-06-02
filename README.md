# NYC 311 Complaint Summarizer

A small Python command-line tool that summarizes recent NYC 311 complaint types using NYC Open Data.

The program queries the NYC 311 Service Requests dataset and prints the most common complaint types over a recent time window.

## Data Source

This project uses NYC Open Data's 311 Service Requests dataset:

- Dataset: 311 Service Requests from 2020 to Present
- API endpoint: `https://data.cityofnewyork.us/resource/erm2-nwe9.json`

## Setup

Clone this repository:

```bash
git clone https://github.com/wintony/nyc-311-complaint-summarizer
cd nyc-311-complaint-summarizer
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the script with:

```bash
python nyc_complaints.py
```

By default, this summarizes complaint types across all of NYC over the last 7 days.

Example:

```bash
python nyc_complaints.py --borough BROOKLYN --days 30 --top 3
```

Example output:

```text
Top 311 complaints in BROOKLYN over the last 30 days

1. Illegal Parking: 20280
2. Noise - Residential: 10372 
3. Blocked Driveway: 5643
```

## Arguments

### `--borough`

Only include complaints from a specific borough.

Valid boroughs:

```text
BRONX
BROOKLYN
MANHATTAN
QUEENS
STATEN ISLAND
```

Example:

```bash
python nyc_complaints.py --borough QUEENS
```

### `--zip`

Only include complaints from a specific 5-digit ZIP code.

Example:

```bash
python nyc_complaints.py --zip 10451
```

Note: `--borough` and `--zip` cannot be used together.

### `--days`

Number of recent days to query.

Default: `7`  
Allowed range: `2` to `365`

Example:

```bash
python nyc_complaints.py --days 30
```

### `--top`

Maximum number of complaint types to show.

If omitted, the program shows all complaint types returned by the query.

Example:

```bash
python nyc_complaints.py --top 10
```

### `--min-count`

Only show complaint types with at least this many reports.

Default: `1`

Example:

```bash
python nyc_complaints.py --min-count 100
```

## Example Commands

Show recent complaint types across all NYC:

```bash
python nyc_complaints.py
```

Show the top 10 complaint types in Brooklyn over the last 30 days:

```bash
python nyc_complaints.py --borough BROOKLYN --days 30 --top 10
```

Show complaint types in a ZIP code:

```bash
python nyc_complaints.py --zip 10451 --days 14
```

Show only complaint types with at least 50 reports:

```bash
python nyc_complaints.py --borough MANHATTAN --days 30 --min-count 50
```