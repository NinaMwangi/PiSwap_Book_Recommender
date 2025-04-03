from pymongo import MongoClient
import pickle
from src.utils.config import MONGODB_URI
import certifi
from datetime import datetime
import numpy as np
import logging
from typing import Dict, Any, Union, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class _MongoDB:
    """Private MongoDB connection class"""
    def __init__(self):
        try:
            logger.info(f"Connecting to MongoDB...")
            self.client = MongoClient(
                MONGODB_URI,
                tls=False,
                connectTimeoutMS=1000,
                socketTimeoutMS=1000,
                retryWrites=True,
                w='majority'
            )
            self.client.admin.command('ping')  # Test connection
            self.db = self.client['book_recommender']
            logger.info("MongoDB connection established")
        except Exception as e:
            logger.error(f"Connection failed: {str(e)}")
            raise

    def get_book_metadata(self, title: str) -> Dict[str, Any]:
        """Get book metadata by title"""
        try:
            book = self.db.final_dataset.find_one({"title": title})
            if not book:
                book = self.db.final_dataset.find_one({
                    "title": {"$regex": f"^{title}$", "$options": "i"}
                })
            return book or {}
        except Exception as e:
            logger.error(f"Metadata lookup failed: {e}")
            return {}

    def update_pivot(self, pivot_df) -> None:
        """Update pivot table in database"""
        self.db['book_pivot'].replace_one(
            {'_id': 'current_pivot'},
            {
                '_id': 'current_pivot',
                'books': pivot_df.index.tolist(),
                'data': pivot_df.values.tolist(),
                'metadata': {
                    'shape': f'{pivot_df.shape}',
                    'updated_at': datetime.utcnow()
                }
            },
            upsert=True
        )

    def load_pivot(self) -> Dict[str, Union[np.ndarray, List[str]]]:
        """Load pivot table from database"""
        pivot_data = self.db['book_pivot'].find_one({'_id': 'current_pivot'})
        if not pivot_data:
            raise ValueError('No pivot table found')
        return {
            'data': np.array(pivot_data['data']),
            'books': pivot_data['books'],
            'user_ids': pivot_data.get('user_ids', [])
        }

    def save_model(self, model, book_names: List[str]) -> None:
        """Save trained model to database"""
        self.db['model_artifacts'].replace_one(
            {'_id': 'knn_model'},
            {
                '_id': 'knn_model',
                'model': pickle.dumps(model),
                'book_names': book_names,
                'trained_at': datetime.utcnow()
            },
            upsert=True
        )

    def load_model(self) -> Dict[str, Any]:
        """Load trained model from database"""
        model_data = self.db['model_artifacts'].find_one({'_id': 'knn_model'})
        if not model_data:
            raise ValueError('No trained model found')
        return {
            'model': pickle.loads(model_data['model']),
            'book_names': model_data['book_names']
        }

# Singleton instance
_mongo_instance = _MongoDB()

def get_db() -> _MongoDB:
    """Get the MongoDB instance"""
    return _mongo_instance