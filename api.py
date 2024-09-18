# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

DB_CONFIG = "dbname=github_ranking user=mjomba password=1234 host=localhost"


class Repo(BaseModel):
    name: str
    description: Optional[str]
    stars: int
    language: Optional[str]
    categories: List[str]
    rank: float

@app.get("/repos", response_model=List[Repo])
async def get_repos(category: Optional[str] = None, min_stars: int = 1000):
    conn = psycopg2.connect(DB_CONFIG)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    query = """
    SELECT r.*, array_agg(c.name) as categories
    FROM repositories r
    LEFT JOIN repo_categories rc ON r.id = rc.repo_id
    LEFT JOIN categories c ON rc.category_id = c.id
    WHERE r.stars >= %s
    """
    params = [min_stars]
    
    if category:
        query += " AND c.name = %s"
        params.append(category)
    
    query += " GROUP BY r.id ORDER BY r.stars DESC"
    
    cur.execute(query, params)
    repos = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return repos

@app.get("/categories")
async def get_categories():
    conn = psycopg2.connect(DB_CONFIG)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("SELECT name FROM categories")
    categories = [row['name'] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return categories

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)