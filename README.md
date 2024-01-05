# Ofsted-Reports-Scraper

Scrape all Ofsted reports into custom `/data` folder

## Getting Started

1. `python -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`

Setup your Ofsted search that you want to download reports from [here](https://reports.ofsted.gov.uk/) to generate the base url to download all reports from.

> Note: It will take hours to download all reports and we highly recommend targeting your search. The example below will download all the reports from Secondary Schools within a 3 mile radius from London.

Run the main Python script giving your base url to download all report pdf's into a folder.

For example:

`python main.py https://reports.ofsted.gov.uk/search?q=&location=London%2C+UK&lat=51.5072178&lon=-0.1275862&radius=3&radius=5&level_1_types=1&level_2_types=2&latest_report_date_start=&latest_report_date_end=&status%5B%5D=1`
