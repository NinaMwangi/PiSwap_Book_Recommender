import pandas as pd
from src.utils.mongo_connector import get_db
from fastapi import HTTPException

class DataUploader:
    def __init__(self):
        self.mongo = get_db()

    @staticmethod
    def process_upload(file_path: str):
        '''Handle bulk csv uploads'''
        try:
            try:
                new_data = pd.read_csv(file_path)
            except pd.errors.EmptyDataError:
                raise HTTPException(
                    status_code=422,
                    detail='Uploaded file is empty or not avalid CSV'
                )

            mongo = get_db()

            # Merging with existing data
            existing = pd.DataFrame(list(mongo.db['final_dataset'].find({}, {'_id': 0})))
            updated = pd.concat([existing, new_data]).drop_duplicates()

            # Atomic updates
            mongo.db['final_dataset'].drop()
            mongo.db['final_dataset'].insert_many(updated.to_dict('records'))
    

            return {
                'status': 'success',
                'new_records': int(len(new_data)),
                'total_records': int(len(updated)),
                'duplicates_removed': len(existing) + len(new_data) - len(updated)
                } 
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Data processing failed: {str(e)}'
            )