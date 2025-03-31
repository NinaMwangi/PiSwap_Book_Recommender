from data_loader import load_raw_data
from preprocessing import (
    preprocess_books,
    preprocess_users,
    preprocessing_ratings,
    final_dataset,
    create_pivot_table
)
from pymongo import MongoClient
import pandas as pd

def main():
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
        client = MongoClient("mongodb+srv://Nina:Mongo%40123@cluster0.jww7vvp.mongodb.net/dbname?retryWrites=true&w=majority",
                             tls=True,
                             tlsAllowInvalidCertificates=True)
        db = client['book_recommender']
        # Storing the preproccessed initial data
        '''db["final_dataset"].insert_many(final.to_dict('records'))
        print("Data saved to MongoDB!")'''

        # 5. Loading the existing preprocessed data from MongoDB
        print("Loading preprocessed data from MongoDB...")
        final_ratings = pd.DataFrame(list(db['final_dataset'].find()))

        # Renaming rating_x to rating
        final_ratings = final_ratings.rename(columns={'rating_x': 'rating'})

        # 6. creating the pivot table from my existing function
        book_pivot = create_pivot_table(final_ratings)

        # 7. Updating pivot table (atomic operation)
        db["book_pivot"].replace_one(
            {"_id": "current_pivot"},
            {
                "_id": "current_pivot",
                "books": book_pivot.index.to_list(),
                "user_ids": book_pivot.columns.to_list(),
                "data": book_pivot.values.tolist(),
                "metadata": {
                    "shape": f"{book_pivot.shape}",
                    "last_updated": pd.Timestamp.now().isoformat()
                }
            },
            # Creates if doesnt exist
            upsert=True
        )
        print(f"Successfully updated pivot table (shape: {book_pivot.shape})")

    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
