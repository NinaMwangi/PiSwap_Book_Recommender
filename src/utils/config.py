import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / '.env'

load_dotenv(env_path)
load_dotenv(env_path, override=True)


MONGODB_URI = os.getenv('MONGODB_URI')
print(f"MONGODB_URI: {MONGODB_URI}")

if not MONGODB_URI:
    raise ValueError('Mongo URI not found')

DATA_PATHS = {
    'books': os.path.join('Data', 'raw_data', 'Books.csv'),
    'users': os.path.join('Data', 'raw_data', 'Users.csv'),
    'ratings': os.path.join('Data', 'raw_data', 'Ratings.csv')
}

MODEL_CONFIG = {
    'n_neighbors': 6,
    'metric': 'cosine'
}