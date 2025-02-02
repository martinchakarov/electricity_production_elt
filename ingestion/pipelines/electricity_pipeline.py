# flake8: noqa
import os
import duckdb

import dlt
from dlt.sources.filesystem import readers

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data.db')
DATABASE = duckdb.connect(DB_PATH)
BUCKET_URL = os.path.join(os.path.dirname(DB_PATH), "raw_data")

def load_electricity_csv() -> None:
    """Loads a local csv for electricity production into duckdb"""
    pipeline = dlt.pipeline(
        pipeline_name="electricity_production",
        dataset_name="electricity_production",
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
        load_electricity_csv()
    except Exception as e:
        print(f'Error: {e}')