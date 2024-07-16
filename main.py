from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pydantic import BaseModel
from typing import List
import logging
import asyncio
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = 'dishes.db'

# Database utility functions
def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        logger.info("Database connection established")
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Models
class Dish(BaseModel):
    dishId: str
    dishName: str
    imageUrl: str
    isPublished: bool

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Dish Information Management System API"}

# API Endpoints
@app.get("/dishes", response_model=List[Dish])
def get_dishes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        logger.info("Executing SELECT query to fetch all dishes")
        cursor.execute("SELECT * FROM dishes")
        dishes = cursor.fetchall()
        conn.close()
        logger.info(f"Fetched {len(dishes)} dishes from the database")
        return [dict(dish) for dish in dishes]
    except Exception as e:
        logger.error(f"Error fetching dishes: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/dishes/toggle/{dish_id}")
async def toggle_dish(dish_id: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        logger.info(f"Executing SELECT query to fetch dish with ID {dish_id}")
        cursor.execute("SELECT * FROM dishes WHERE dishId = ?", (dish_id,))
        dish = cursor.fetchone()

        if dish is None:
            logger.warning(f"Dish with ID {dish_id} not found")
            raise HTTPException(status_code=404, detail="Dish not found")

        new_status = not dish["isPublished"]
        logger.info(f"Toggling isPublished status for dish ID {dish_id} to {new_status}")
        cursor.execute("UPDATE dishes SET isPublished = ? WHERE dishId = ?", (new_status, dish_id))
        conn.commit()
        conn.close()

        logger.info(f"Dish status updated successfully for ID {dish_id}")

        # Broadcast the update to all connected clients
        await broadcast_update({"dishId": dish_id, "isPublished": new_status})

        return JSONResponse(content={"message": "Dish status updated", "new_status": new_status})
    except Exception as e:
        logger.error(f"Error toggling dish status: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

subscribers = []

@app.get("/events")
async def sse(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            if subscribers:
                data = subscribers.pop(0)
                yield f"data: {data}\n\n"
            await asyncio.sleep(0.5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

async def broadcast_update(data):
    message = json.dumps(data)
    subscribers.append(message)