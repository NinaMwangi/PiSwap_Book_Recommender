import pandas as pd
import numpy as np
from pymongo import MongoClient

def preprocess_books(books):
    books = books.drop(['Image-URL-S', 'Image-URL-M'], axis=1)
    return books.rename(columns={
        'Book-Title':'title',
        'Book-Author':'author',
        'Year-Of-Publication':'year',
        'Publisher':'publisher',
        'Image-URL-L':'image_url'
    })

def preprocess_users(users):
    users = users.rename(columns={
        'User-ID': 'user_id'
    })[['user_id']]
    return users

def preprocessing_ratings(ratings):
    ratings = ratings.rename(columns={
        'User-ID': 'user_id',
        'Book-Rating': 'rating'
    })

    active_users = ratings['user_id'].value_counts()
    active_users = active_users[active_users > 200].index
    ratings = ratings[ratings['user_id'].isin(active_users)]

    return ratings

def final_dataset(books, users, ratings):
    ''' Merging all datasets'''
    merged = ratings.merge(books, on='ISBN')

    rating_counts = merged.groupby('title')['rating'].count().reset_index()
    rating_counts = rating_counts[rating_counts['rating'] >= 50]
    merged = merged.merge(rating_counts, on='title')

    final = merged.merge(users, left_on='user_id', right_on='user_id')

    final = final.drop_duplicates(['user_id', 'title'])

    return final

def create_pivot_table(final):
    '''Creating user-book rating matrix'''
    print("Creating pivot table...")
    book_pivot = final.pivot_table(
        index='title',
        columns='user_id',
        values='rating',
        fill_value=0
    )
    return book_pivot
