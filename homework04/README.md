# Homework 04 - IMDB Movies Flask API

A REST API built with Flask for querying IMDB movie data.

## Prerequisites
- Python 3.x
- Docker
- Git

## Project Structure
    homework04/
    app.py               - Flask API
    test_app.py          - Pytest tests
    movies.json          - IMDB movie dataset
    requirements.txt     - Python dependencies
    Dockerfile           - Container definition
    README.md            - This file

## API Routes
- GET /movies                              - Return all movies
- GET /movies?start_year=int&end_year=int  - Filter by year range
- GET /movies/top_rated?n=int              - Top N movies by rating
- GET /movies/genre/<genre>                - Filter by genre
- GET /movies/summary                      - Dataset statistics

## Running Locally
1. Create and activate a virtual environment
    python3 -m venv movies
    source movies/bin/activate

2. Install dependencies
    pip install -r requirements.txt

3. Run the Flask app
    python app.py

4. The API will be available at http://localhost:5000

5. Run the tests
    pytest test_app.py -v

## Running with Docker
1. Build the Docker image
    docker build -t homework04 .

2. Run the container
    docker run -d -p 5000:5000 --name hw04 homework04

3. The API will be available at http://localhost:5000

4. Stop the container
    docker stop hw04

## Notes
- All routes include docstrings, type hints, logging, and exception handling.
- Tests are written with pytest and cover all 5 routes plus an invalid endpoint.
