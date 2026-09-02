# COVID-19 Report

A Flask web application that imports the Italian Civil Protection Department
province-level COVID-19 dataset into SQLite and displays total cases
aggregated by Italian region.


## Requirements

- Python 3.9 or newer

## Installation

Create and activate a virtual environment, then install the dependencies:


python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt


## Import the data

The importer creates the SQLite database and loads the JSON dataset:

The importer expects the source file at
`data/json/dpc-covid19-ita-province.json` and creates the database at
`data/db/covid-19.db`.

Running the importer rebuilds the database from the JSON file. Use it when the
source dataset has been replaced or refreshed.

## Run the application

Start Flask after activating the virtual environment:


flask --app app run


Then open http://127.0.0.1:5000 in a browser.

The startup script runs the import and starts the application:


./startup.sh


## Usage

The dashboard shows one row per Italian region. By default, results use the
latest date available in the database and are ordered by total cases in
descending order, with the region name as the secondary ordering key.

The date filter accepts the `YYYY-MM-DD` format. Supported ordering values are:

- `cases_desc`: total cases descending, region ascending as a tie-breaker;
- `cases_asc`: total cases ascending, region ascending as a tie-breaker;
- `reg_asc`: region name ascending;
- `reg_desc`: region name descending.

The export link downloads the selected results as an Excel-compatible `.xls`
file containing one worksheet with the columns `Region` and `Total cases`.



## Data source and availability

The JSON file currently included in this repository was updated on 8 January
2025. Consequently, dates after `2025-01-08` cannot return data until a newer
source file is imported. The historical series starts on 24 February 2020.



