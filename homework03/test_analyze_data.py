"""
test_analyze_data.py

Unit tests for analyze_data.py using pytest.
Tests cover net_profit(), average_rating_by_year(), and top_genres_by_count().
"""

import pytest
from analyze_data import net_profit, average_rating_by_year, top_genres_by_count


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_data():
    """Standard sample dataset used across multiple tests."""
    return [
        {"Title": "Movie A", "budget": 1000000,  "grossWorldWide": 5000000,  "Rating": 7.5, "Year": 2021, "genres": ["Action", "Drama"]},
        {"Title": "Movie B", "budget": 500000,   "grossWorldWide": 10000000, "Rating": 8.0, "Year": 2021, "genres": ["Comedy"]},
        {"Title": "Movie C", "budget": 2000000,  "grossWorldWide": 3000000,  "Rating": 6.0, "Year": 2022, "genres": ["Action"]},
        {"Title": "Movie D", "budget": 100000,   "grossWorldWide": 200000,   "Rating": 5.5, "Year": 2022, "genres": ["Horror"]},
        {"Title": "Movie E", "budget": 50000000, "grossWorldWide": 200000000,"Rating": 9.0, "Year": 2023, "genres": ["Action", "Comedy"]},
    ]

@pytest.fixture
def single_movie():
    """Dataset with only one movie."""
    return [
        {"Title": "Solo Film", "budget": 100000, "grossWorldWide": 900000, "Rating": 7.0, "Year": 2020, "genres": ["Drama"]},
    ]

@pytest.fixture
def missing_fields_data():
    """Dataset where some records are missing budget/gross/rating fields."""
    return [
        {"Title": "Incomplete A", "budget": None,   "grossWorldWide": None,   "Rating": None, "Year": 2021, "genres": []},
        {"Title": "Incomplete B", "budget": 100000, "grossWorldWide": 500000, "Rating": 6.5,  "Year": 2021, "genres": "Drama"},
        {"Title": "Incomplete C", "budget": 200000, "grossWorldWide": 800000, "Rating": 7.0,  "Year": 2022, "genres": ["Thriller"]},
    ]


# ---------------------------------------------------------------------------
# Tests for net_profit()
# ---------------------------------------------------------------------------

class TestNetProfit:

    def test_correct_winner(self, sample_data):
        """Movie E has the highest net profit (150,000,000)."""
        result = net_profit(sample_data)
        assert result == "Movie E"

    def test_single_movie_returns_that_movie(self, single_movie):
        """With one movie, it must be returned regardless of profit."""
        result = net_profit(single_movie)
        assert result == "Solo Film"

    def test_empty_data_raises_value_error(self):
        """Empty list should raise a ValueError."""
        with pytest.raises(ValueError):
            net_profit([])

    def test_handles_none_budget_fields(self, missing_fields_data):
        """Movies with None values should be skipped; valid ones still processed."""
        result = net_profit(missing_fields_data)
        assert result in ["Incomplete B", "Incomplete C"]

    def test_returns_string(self, sample_data):
        """Return type should always be a string."""
        result = net_profit(sample_data)
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# Tests for average_rating_by_year()
# ---------------------------------------------------------------------------

class TestAverageRatingByYear:

    def test_correct_average(self, sample_data):
        """2021 average should be (7.5 + 8.0) / 2 = 7.75."""
        result = average_rating_by_year(sample_data)
        assert result[2021] == 7.75

    def test_all_years_present(self, sample_data):
        """All three years in the sample should appear in the result."""
        result = average_rating_by_year(sample_data)
        assert 2021 in result
        assert 2022 in result
        assert 2023 in result

    def test_single_movie_year(self, single_movie):
        """A year with one movie should return that movie's exact rating."""
        result = average_rating_by_year(single_movie)
        assert result[2020] == 7.0

    def test_empty_data_raises_value_error(self):
        """Empty list should raise a ValueError."""
        with pytest.raises(ValueError):
            average_rating_by_year([])

    def test_returns_dict(self, sample_data):
        """Return type should be a dictionary."""
        result = average_rating_by_year(sample_data)
        assert isinstance(result, dict)

    def test_values_are_floats(self, sample_data):
        """All values in the result dict should be floats."""
        result = average_rating_by_year(sample_data)
        for val in result.values():
            assert isinstance(val, float)


# ---------------------------------------------------------------------------
# Tests for top_genres_by_count()
# ---------------------------------------------------------------------------

class TestTopGenresByCount:

    def test_action_is_most_common(self, sample_data):
        """Action appears in 3 movies and should rank first."""
        result = top_genres_by_count(sample_data)
        top_genre = next(iter(result))
        assert top_genre == "Action"

    def test_all_genres_present(self, sample_data):
        """All genres in the dataset should appear in the result."""
        result = top_genres_by_count(sample_data)
        assert "Action" in result
        assert "Comedy" in result
        assert "Drama" in result
        assert "Horror" in result

    def test_genre_as_string_handled(self, missing_fields_data):
        """A genre stored as a plain string should still be counted."""
        result = top_genres_by_count(missing_fields_data)
        assert "Drama" in result

    def test_empty_data_raises_value_error(self):
        """Empty list should raise a ValueError."""
        with pytest.raises(ValueError):
            top_genres_by_count([])

    def test_returns_dict(self, sample_data):
        """Return type should be a dictionary."""
        result = top_genres_by_count(sample_data)
        assert isinstance(result, dict)

    def test_values_are_integers(self, sample_data):
        """All count values should be integers."""
        result = top_genres_by_count(sample_data)
        for val in result.values():
            assert isinstance(val, int)
