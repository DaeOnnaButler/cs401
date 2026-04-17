# Homework 03 - IMDB Movie Data Analysis

Analyzes IMDB movie data to find the highest net-profit film, average ratings by year, and most common genres.

## Prerequisites
- Python 3.x
- Docker
- Git

## Project Structure
    homework03/
    analyze_data.py       - Main analysis script
    test_analyze_data.py  - Pytest unit tests
    data.json             - IMDB movie dataset
    requirements.txt      - Python dependencies
    Dockerfile            - Container definition
    README.md             - This file

## Running Locally
1. Create and activate a virtual environment
    python3 -m venv imdb
    source imdb/bin/activate

2. Install dependencies
    pip install -r requirements.txt

3. Run the analysis
    python analyze_data.py data.json

4. Run the tests
    pytest test_analyze_data.py -v

## Running with Docker
1. Build the image
    docker build -t homework03 .

2. Run the analysis
    docker run --rm homework03

3. Run the tests
    docker run --rm homework03 pytest test_analyze_data.py -v

## What the Program Does
- read_json(): Loads data.json into memory
- net_profit(): Returns the movie with the highest gross minus budget
- average_rating_by_year(): Prints the mean IMDB rating per year
- top_genres_by_count(): Prints the most common genres across all movies

## Notes
- All functions include docstrings, type hints, logging, and exception handling.
- Tests cover normal cases, edge cases, and error conditions.
