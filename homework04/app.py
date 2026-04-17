"""
app.py

A Flask API for querying IMDB movie data.
"""

import json
import logging
from flask import Flask, jsonify, request

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def load_movies() -> list:
    """Load movies from the JSON file."""
    with open("movies.json", "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/movies", methods=["GET"])
def get_movies() -> tuple:
    """
    Return all movies or filter by release year range.

    Description:
        Returns the full movie dataset. Optionally accepts start_year
        and end_year query parameters to filter results by release year.

    Args:
        start_year (int, optional): The earliest release year to include.
        end_year (int, optional): The latest release year to include.

    Returns:
        tuple: A JSON response containing a list of movies and an HTTP status code.

    Raises:
        ValueError: If start_year or end_year cannot be converted to integers.
    """
    logger.debug("GET /movies called with args: %s", request.args)
    try:
        movies = load_movies()
        start_year = request.args.get("start_year")
        end_year = request.args.get("end_year")

        if start_year or end_year:
            start_year = int(start_year) if start_year else 0
            end_year = int(end_year) if end_year else 9999
            movies = [m for m in movies if start_year <= m.get("Year", 0) <= end_year]

        return jsonify(movies), 200

    except ValueError as e:
        logger.error("Invalid year parameter: %s", e)
        return jsonify({"error": "start_year and end_year must be integers"}), 400


@app.route("/movies/top_rated", methods=["GET"])
def get_top_rated() -> tuple:
    """
    Return the top N movies sorted by IMDB rating.

    Description:
        Returns movies sorted in descending order by Rating.
        The number of results can be controlled with the query parameter n.

    Args:
        n (int, optional): Number of top rated movies to return. Defaults to 10.

    Returns:
        tuple: A JSON response containing a list of top rated movies and an HTTP status code.

    Raises:
        ValueError: If n cannot be converted to an integer.
    """
    logger.debug("GET /movies/top_rated called with args: %s", request.args)
    try:
        movies = load_movies()
        n = int(request.args.get("n", 10))
        sorted_movies = sorted(movies, key=lambda m: float(m.get("Rating") or 0), reverse=True)
        return jsonify(sorted_movies[:n]), 200

    except ValueError as e:
        logger.error("Invalid n parameter: %s", e)
        return jsonify({"error": "n must be an integer"}), 400


@app.route("/movies/genre/<string:genre>", methods=["GET"])
def get_by_genre(genre: str) -> tuple:
    """
    Return all movies that belong to a specific genre.

    Description:
        Filters the dataset by the given genre string (case-insensitive)
        and returns all matching movies.

    Args:
        genre (str): The genre name to filter by (e.g. Drama, Action).

    Returns:
        tuple: A JSON response containing a list of matching movies and an HTTP status code.

    Raises:
        ValueError: If the genre results in an unexpected filtering error.
    """
    logger.debug("GET /movies/genre/%s called", genre)
    try:
        movies = load_movies()
        filtered = [m for m in movies if genre.lower() in [g.lower() for g in m.get("genres", [])]]
        return jsonify(filtered), 200

    except ValueError as e:
        logger.error("Error filtering by genre: %s", e)
        return jsonify({"error": "Could not filter by genre"}), 400


@app.route("/movies/summary", methods=["GET"])
def get_summary() -> tuple:
    """
    Return a summary of statistics about the movie dataset.

    Description:
        Computes and returns the total number of movies, average IMDB
        rating, and average budget across the entire dataset.

    Args:
        None

    Returns:
        tuple: A JSON response containing summary statistics and an HTTP status code.

    Raises:
        ZeroDivisionError: If the dataset is empty.
    """
    logger.debug("GET /movies/summary called")
    try:
        movies = load_movies()
        if not movies:
            raise ZeroDivisionError("No movies in dataset.")

        avg_rating = round(sum(float(m.get("Rating") or 0) for m in movies) / len(movies), 2)
        budgets = [m.get("budget", 0) for m in movies if m.get("budget")]
        avg_budget = round(sum(budgets) / len(budgets), 2) if budgets else 0

        return jsonify({
            "total_movies": len(movies),
            "average_rating": avg_rating,
            "average_budget": avg_budget
        }), 200

    except ZeroDivisionError as e:
        logger.error("ZeroDivisionError in summary: %s", e)
        return jsonify({"error": "No movies in dataset"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
