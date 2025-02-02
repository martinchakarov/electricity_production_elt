import os
import duckdb
from typing import Any, Optional

import dlt
from dlt.sources.rest_api import (
    RESTAPIConfig,
    check_connection,
    rest_api_resources,
    rest_api_source,
)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data.db')
DATABASE = duckdb.connect(DB_PATH)


@dlt.source(name="rest_countries", max_table_nesting=0)
def countries_source(access_token: Optional[str] = dlt.secrets.value) -> Any:
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://restcountries.com/v3.1"
        },
        "resource_defaults": {
            "write_disposition": "replace",
            "endpoint": {
                "params": {
                    "per_page": 100,
                }
            }
        },
        "resources": [
            {
                "name": "countries",
                "endpoint": {
                    "path": "all",
                    "paginator": "single_page"
                }
            }
        ]
    }

    yield from rest_api_resources(config)


def load_countries_data() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="rest_countries",
        dataset_name="electricity_production",
        destination=dlt.destinations.duckdb(DATABASE),
        progress='log'
    )

    load_info = pipeline.run(countries_source())
    print(load_info) 

    DATABASE.close()

if __name__ == "__main__":
    try:
        load_countries_data()
    except Exception as e:
        print(f'Error: {e}')