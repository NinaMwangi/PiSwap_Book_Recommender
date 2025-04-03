from sklearn.neighbors import NearestNeighbors
from src.utils.mongo_connector import _MongoDB as MongoDB
from src.utils.config import MODEL_CONFIG
import numpy as np
import pickle
from datetime import datetime

def train_model():
    mongo = MongoDB()
    try:
        pivot = mongo.load_pivot()
        print(f"Loaded pivot data with shape: {pivot['data'].shape}")
    except Exception as e:
        print(f"Failed to load pivot: {str(e)}")
        raise

    try:
        model = NearestNeighbors(**MODEL_CONFIG)
        model.fit(pivot['data'])
        print("Model trained successfully")
    except Exception as e:
        print(f"Model training failed: {str(e)}")
        raise

    try:
        mongo.save_model(model, pivot['books'])
        print('model saved successfully')
    except Exception as e:
        print(f"Failed to save model: {str(e)}")
        raise

if __name__ == "__main__":
    train_model()
