from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import sqlite3
from pydantic import BaseModel
from typing import List

app = FastAPI()

DATABASE = 'dishes.db'

# Database utility functions
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Models
class Dish(BaseModel):
    dishId: str
    dishName: str
    imageUrl: str
    isPublished: bool

# API Endpoints
@app.get("/dishes", response_model=List[Dish])
def get_dishes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dishes")
    dishes = cursor.fetchall()
    conn.close()

    return [dict(dish) for dish in dishes]

@app.post("/dishes/toggle/{dish_id}")
def toggle_dish(dish_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dishes WHERE dishId = ?", (dish_id,))
    dish = cursor.fetchone()

    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")

    new_status = not dish["isPublished"]
    cursor.execute("UPDATE dishes SET isPublished = ? WHERE dishId = ?", (new_status, dish_id))
    conn.commit()
    conn.close()

    return JSONResponse(content={"message": "Dish status updated", "new_status": new_status})

# To run the app, use the command:
    uvicorn main:app --reload
