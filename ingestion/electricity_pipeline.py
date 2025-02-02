# flake8: noqa
import os
import duckdb

import dlt
from dlt.sources import TDataItems
from dlt.sources.filesystem import readers

BUCKET_URL = os.path.join(os.getcwd(), "raw_data")
DATABASE = duckdb.connect(os.path.join(os.getcwd(), "data.db"))

def load_csv() -> None:
    """Loads a local csv for electricity production into duckdb"""
    pipeline = dlt.pipeline(
        pipeline_name="electricity_production",
        dataset_name="weather_vs_electricity_production",
        destination=dlt.destinations.duckdb(DATABASE),
        progress='log'
    )

    local_file = readers(bucket_url=BUCKET_URL, file_glob="electricity_production.csv").read_csv_duckdb()
    local_file.apply_hints(write_disposition="replace")
    load_info = pipeline.run(local_file.with_name("electricity_production"))
    print(load_info)

    DATABASE.close()

if __name__ == "__main__":
    try:
        load_csv()
    except Exception as e:
        print(f'Error: {e}')