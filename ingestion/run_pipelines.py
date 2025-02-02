import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "pipelines"))
from rest_api_pipeline import load_countries_data
from electricity_pipeline import load_electricity_csv

if __name__ == "__main__":
    try:
        print('\nLoading countries data...\n')
        load_countries_data()
        print('\nLoading electricity data...\n')
        load_electricity_csv()
    except Exception as e:
        print(f'Error: {e}')