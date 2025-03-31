import pandas as pd

def load_raw_data():
    '''Loading all CSV files to into Dataframes'''
    try: 
        return{
            'books': pd.read_csv('/Users/nina/PiSwap_Book_Recommender/Data/raw_data/Books.csv', low_memory=False),
            'users': pd.read_csv('/Users/nina/PiSwap_Book_Recommender/Data/raw_data/Users.csv'),
            'ratings': pd.read_csv('/Users/nina/PiSwap_Book_Recommender/Data/raw_data/Ratings.csv')
        }
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        raise

'''if __name__ == "__main__":
    load_raw_data()'''