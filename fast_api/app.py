from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Create FastAPI instance
app = FastAPI()

# Define a model for the movie
class Movie(BaseModel):
    title: str
    release_date: str
    score: float
    comment: Optional[str] = None

# Database to store movies
movies_db = []

# CRUD operations for movies
@app.post("/movies/")
def create_movie(movie: Movie):
    movies_db.append(movie)
    return {"message": "Movie created successfully"}

@app.get("/movies/", response_model=List[Movie])
def read_movies():
    return movies_db

@app.get("/movies/{movie_id}", response_model=Movie)
def read_movie(movie_id: int):
    try:
        return movies_db[movie_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Movie not found")

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: Movie):
    try:
        movies_db[movie_id] = movie
        return {"message": "Movie updated successfully"}
    except IndexError:
        raise HTTPException(status_code=404, detail="Movie not found")

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    try:
        del movies_db[movie_id]
        return {"message": "Movie deleted successfully"}
    except IndexError:
        raise HTTPException(status_code=404, detail="Movie not found")
