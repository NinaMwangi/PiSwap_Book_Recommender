from .utils.mongo_connector import _MongoDB as MongoDB
import numpy as np
from typing import List, Dict


class BookRecommender:
    def __init__(self):
        self.mongo = MongoDB()
        self.load_model()

    def load_model(self):
        '''Loading model & metadata from MongoDB'''
        artifacts = self.mongo.load_model()
        self.model = artifacts['model']
        self.book_names = artifacts['book_names']

        # Precomputing the indices for faster lookup
        self.book_to_index = {book: idx for idx, book in enumerate(
            self.book_names
        )}

    def recommend(self, book_title: str) -> List[Dict]:
        ''' Getting top 5 recommendations with similarity scores'''
        try:
            
            book_idx = self.book_to_index[book_title]
            print(book_idx)
            distances, indices = self.model.kneighbors(
                self.model._fit_X[book_idx].reshape(1, -1)
            )
            return [
                {
                    'title': self.book_names[idx],
                    'score': float(1 - dist),
                    'rank': i + 1
                }
                for i, (dist, idx) in enumerate(zip(distances[0][1:6], 
                                                    indices[0][1:6]))
            ]
        except KeyError:
            return [{'error': f"Book '{book_title}' not found in database"}]
        except Exception as e:
            return [{'error': str(e)}]