from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from typing import List, Optional

# Create FastAPI instance
app = FastAPI()

# Define a model for the movie
class Movie(BaseModel):
    title: str
    release_date: str
    score: float
    comment: Optional[str] = None

# Database connection URL for SQLite (in-memory database)
DATABASE_URL = "sqlite:///./test.db"

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define a table for the movies
movies = Table(
    "movies",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("release_date", String),
    Column("score", Float),
    Column("comment", String),
)

# Create the database tables
metadata.create_all(engine)

# Dependency for database connection
async def get_database():
    async with Database(DATABASE_URL) as database:
        yield database

# CRUD operations for movies

# Create a movie
@app.post("/movies/")
async def create_movie(movie: Movie, database: Database = Depends(get_database)):
    query = movies.insert().values(
        title=movie.title, release_date=movie.release_date, score=movie.score, comment=movie.comment
    )
    last_record_id = await database.execute(query)
    return {"message": "Movie created successfully"}

# Read all movies
@app.get("/movies/", response_model=List[Movie])
async def read_movies(database: Database = Depends(get_database)):
    query = movies.select()
    return await database.fetch_all(query)

# Read a single movie by ID
@app.get("/movies/{movie_id}", response_model=Movie)
async def read_movie(movie_id: int, database: Database = Depends(get_database)):
    query = movies.select().where(movies.c.id == movie_id)
    movie = await database.fetch_one(query)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# Update a movie by ID
@app.put("/movies/{movie_id}")
async def update_movie(movie_id: int, movie: Movie, database: Database = Depends(get_database)):
    query = movies.update().where(movies.c.id == movie_id).values(
        title=movie.title, release_date=movie.release_date, score=movie.score, comment=movie.comment
    )
    await database.execute(query)
    return {"message": "Movie updated successfully"}

# Delete a movie by ID
@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int, database: Database = Depends(get_database)):
    query = movies.delete().where(movies.c.id == movie_id)
    await database.execute(query)
    return {"message": "Movie deleted successfully"}

