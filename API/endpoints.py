from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.prediction import BookRecommender
from src.train import train_model
from src.pipeline import run_pipeline
from src.upload import DataUploader
from src.utils.mongo_connector import get_db
import tempfile
import os
from fastapi.responses import JSONResponse
import json
app = FastAPI()
mongo = get_db()  # Get the singleton instance

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

@app.post('/api/upload')
async def upload_csv(file: UploadFile, background_tasks: BackgroundTasks):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        upload_result = DataUploader.process_upload(tmp_path)
        background_tasks.add_task(lambda: os.unlink(tmp_path))
        background_tasks.add_task(run_pipeline)
        background_tasks.add_task(train_model)
        
        return JSONResponse({
            'message': 'Upload successful',
            'data': upload_result
        })
    except Exception as e:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(500, detail=str(e))

@app.get('/api/recommend/{book_title}')
async def get_recommendations(book_title: str):
    try:
        # breakpoint()
        recommender = BookRecommender()
        
        if not mongo.db.final_dataset.find_one({"title": book_title}):
            return {"error": f"Book '{book_title}' not found"}
        
        results = recommender.recommend(book_title)
        
        for book in results:
            metadata = mongo.get_book_metadata(book['title'])
            metadata.pop("_id",None)
            book.update({
                'metadata': metadata,
                'from_collection': 'final_dataset'
            })
            
            
        return {
            'recommendations': results,
            'searched_title': book_title
        }
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@app.get('/debug/mongo')
async def debug_mongo():
    try:
        return {
            "collections": mongo.db.list_collection_names(),
            "book_count": mongo.db.final_dataset.count_documents({})
        }
    except Exception as e:
        return {"error": str(e)}

@app.get('/api/training-status')
async def training_status():
    try:
        model_data = mongo.db.model_artifacts.find_one({"_id": "knn_model"})
        return {
            "status": "success",
            "last_trained": model_data.get("trained_at") if model_data else None,
            "book_count": len(model_data.get("book_names", [])) if model_data else 0
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))