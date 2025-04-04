import os
import sys
import pandas as pd
from src.utils.config import DATA_PATHS



from src.utils.config import DATA_PATHS


def load_raw_data():
    '''Loading all CSV files to into Dataframes'''

    try: 
        return{
            'books': pd.read_csv(DATA_PATHS['books'], low_memory=False),
            'users': pd.read_csv(DATA_PATHS['users']),
            'ratings': pd.read_csv(DATA_PATHS['ratings'])
        }
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        raise

# if __name__ == "__main__":
#     load_raw_data()