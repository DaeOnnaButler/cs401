"""
test_app.py

Unit tests for app.py Flask API using pytest.
Tests cover all 5 routes and one invalid endpoint.
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_all_movies(client):
    """Test that /movies returns all movies with status 200."""
    response = client.get("/movies")
    data = response.get_json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_movies_by_year_range(client):
    """Test that /movies?start_year=2021&end_year=2022 filters correctly."""
    response = client.get("/movies?start_year=2021&end_year=2022")
    data = response.get_json()
    assert response.status_code == 200
    assert all(2021 <= m["Year"] <= 2022 for m in data)


def test_get_movies_invalid_year(client):
    """Test that non-integer year params return a 400 error."""
    response = client.get("/movies?start_year=abc")
    data = response.get_json()
    assert response.status_code == 400
    assert "error" in data


def test_get_top_rated(client):
    """Test that /movies/top_rated returns top N movies sorted by rating."""
    response = client.get("/movies/top_rated?n=5")
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 5
    ratings = [m["Rating"] for m in data]
    assert ratings == sorted(ratings, reverse=True)


def test_get_by_genre(client):
    """Test that /movies/genre/Drama returns only Drama movies."""
    response = client.get("/movies/genre/Drama")
    data = response.get_json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert all("Drama" in m.get("genres", []) for m in data)


def test_get_summary(client):
    """Test that /movies/summary returns correct summary statistics."""
    response = client.get("/movies/summary")
    data = response.get_json()
    assert response.status_code == 200
    assert "total_movies" in data
    assert "average_rating" in data
    assert "average_budget" in data


def test_invalid_endpoint(client):
    """Test that an invalid endpoint returns a 404 error."""
    response = client.get("/invalid_endpoint")
    assert response.status_code == 404
