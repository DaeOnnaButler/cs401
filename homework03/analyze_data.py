"""
analyze_data.py

Analyzes IMDB movie data from a JSON file, computing statistics such as
highest net profit, average rating by year, and most common genres.
"""

import json
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def read_json(filepath: str) -> list:
    """
    Reads a JSON file and returns the data as a list of dictionaries.

    Description:
        Opens and parses the specified JSON file containing IMDB movie data.

    Args:
        filepath (str): The path to the JSON file to read.

    Returns:
        list: A list of movie records loaded from the JSON file.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
    """
    logger.debug("Attempting to read JSON file from path: %s", filepath)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.debug("Successfully loaded %d records from %s", len(data), filepath)
        return data
    except FileNotFoundError as e:
        logger.error("File not found: %s", filepath)
        raise FileNotFoundError(f"Could not find data file at '{filepath}'") from e


def net_profit(data: list) -> str:
    """
    Finds the movie with the highest net profit.

    Description:
        Iterates through all movies and calculates net profit as
        (grossWorldWide - budget), returning the title of the movie
        with the greatest net profit.

    Args:
        data (list): A list of movie records, each containing
                     'Title', 'budget', and 'grossWorldWide' fields.

    Returns:
        str: The title of the movie with the highest net profit.

    Raises:
        ValueError: If the data list is empty or no valid profit entries exist.
    """
    logger.debug("Calculating net profit across %d movies", len(data))
    try:
        if not data:
            raise ValueError("Data list is empty.")

        best_movie = None
        best_profit = float("-inf")

        for movie in data:
            try:
                budget = float(movie.get("budget") or 0)
                gross = float(movie.get("grossWorldWide") or 0)
                profit = gross - budget
                if profit > best_profit:
                    best_profit = profit
                    best_movie = movie.get("Title", "Unknown")
            except (TypeError, ValueError):
                continue

        if best_movie is None:
            raise ValueError("No valid profit data found in dataset.")

        logger.debug("Highest net profit movie: %s with profit $%.2f", best_movie, best_profit)
        return best_movie

    except ValueError as e:
        logger.error("ValueError in net_profit: %s", e)
        raise


def average_rating_by_year(data: list) -> dict:
    """
    Computes the average IMDB rating for movies grouped by release year.

    Description:
        Iterates through the dataset and calculates the mean Rating for
        each Year, giving insight into how overall movie quality has
        changed over time.

    Args:
        data (list): A list of movie records, each containing
                     'Year' and 'Rating' fields.

    Returns:
        dict: A dictionary mapping each year (int) to its average
              rating (float), rounded to 2 decimal places.

    Raises:
        ValueError: If the data list is empty.
    """
    logger.debug("Computing average rating by year for %d movies", len(data))
    try:
        if not data:
            raise ValueError("Data list is empty.")

        year_totals = {}

        for movie in data:
            year = movie.get("Year")
            try:
                rating = float(movie.get("Rating") or 0)
                if year not in year_totals:
                    year_totals[year] = []
                year_totals[year].append(rating)
            except (TypeError, ValueError):
                continue

        averages = {
            year: round(sum(ratings) / len(ratings), 2)
            for year, ratings in year_totals.items() if ratings
        }

        logger.debug("Average ratings computed for years: %s", list(averages.keys()))
        print("\n--- Average IMDB Rating by Year ---")
        for year, avg in sorted(averages.items()):
            print(f"  {year}: {avg}")

        return averages

    except ValueError as e:
        logger.error("ValueError in average_rating_by_year: %s", e)
        raise


def top_genres_by_count(data: list) -> dict:
    """
    Counts and ranks how many movies belong to each genre.

    Description:
        Iterates through all movies and tallies genre occurrences,
        printing the top 5 most common genres across the dataset.

    Args:
        data (list): A list of movie records, each containing
                     a 'genres' field (list of strings).

    Returns:
        dict: A dictionary of genre names mapped to their movie counts,
              sorted in descending order.

    Raises:
        ValueError: If the data list is empty.
    """
    logger.debug("Counting movies per genre across %d records", len(data))
    try:
        if not data:
            raise ValueError("Data list is empty.")

        genre_counts = {}

        for movie in data:
            genres = movie.get("genres", [])
            if isinstance(genres, str):
                genres = [genres]
            for genre in genres:
                genre = genre.strip()
                if genre:
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1

        sorted_genres = dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True))

        logger.debug("Top genre: %s", next(iter(sorted_genres), "N/A"))
        print("\n--- Top 5 Most Common Genres ---")
        for genre, count in list(sorted_genres.items())[:5]:
            print(f"  {genre}: {count} movies")

        return sorted_genres

    except ValueError as e:
        logger.error("ValueError in top_genres_by_count: %s", e)
        raise


def main():

    if len(sys.argv) < 2:
        print("Error: No command line argument provided. Please provide a file name for a json file to read. i.e. python analyze_data.py data.json")
        sys.exit(1)

    output_file = sys.argv[1]

    data = read_json(output_file)

    net_profit_answer = net_profit(data)
    print(f'Movie with largest net profit: {net_profit_answer}')

    avg_ratings = average_rating_by_year(data)

    top_genres = top_genres_by_count(data)


if __name__ == '__main__':
    main()
