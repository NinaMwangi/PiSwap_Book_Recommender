from src.data_loader import load_raw_data
from src.preprocessing import (
    preprocess_books,
    preprocess_users,
    preprocessing_ratings,
    final_dataset,
    create_pivot_table
)
import pandas as pd
from src.utils.mongo_connector import get_db




def run_pipeline():
    try:
        # 1. Load Data
        print('Loading raw data...')
        raw_data = load_raw_data()

        # 2. Preprocess
        print('preprocesssing...')
        books = preprocess_books(raw_data['books'])
        users = preprocess_users(raw_data['users'])
        ratings = preprocessing_ratings(raw_data['ratings'])

        # 3. Merge
        print('Creating final dataset...')
        final = final_dataset(books, users, ratings)

        print(f"Final dataset shape: {final.shape}")
        print(f" Sample data:\n{final.head(2)}")

        # 4. Connecting to MongoDB 
        # mongo = MongoDB()
        mongo = get_db()
       
        # Storing the preproccessed initial data
        mongo.db["final_dataset"].insert_many(final.to_dict('records'))
        print("Data saved to MongoDB!")

        # 5. Loading the existing preprocessed data from MongoDB
        print("Loading preprocessed data from MongoDB...")
        final_ratings = pd.DataFrame(list(mongo.db['final_dataset'].find()))

        # Renaming rating_x to rating
        final_ratings = final_ratings.rename(columns={'rating_x': 'rating'})

        # 6. creating the pivot table from my existing function
        book_pivot = create_pivot_table(final_ratings)
        mongo.update_pivot(book_pivot)
   
    except Exception as e:
        print(f"Error: {e}")

def trigger_retraining(async_mode = True):
    ''' One click retraining'''
    def _train():
        from train import train_model
        train_model()

    if async_mode:
        import threading
        threading.Thread(target=_train).start()
        return {'status': 'Retraining started'}
    return _train()

if __name__ == "__main__":
    run_pipeline()
