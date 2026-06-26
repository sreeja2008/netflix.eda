"""
Generates a synthetic Netflix-style catalog dataset, structured exactly like
the well-known public "Netflix Movies and TV Shows" dataset on Kaggle
(columns: show_id, type, title, director, cast, country, date_added,
release_year, rating, duration, listed_in, description).

Why synthetic: this environment has no internet access to download the real
CSV. The structure, column names, and realistic value distributions match
the real dataset closely, so every technique you practice here (cleaning,
grouping, plotting) transfers directly once you swap in the real file.

To use the REAL dataset instead:
1. Go to: https://www.kaggle.com/datasets/shivamb/netflix-shows
2. Download netflix_titles.csv
3. Drop it into this same folder, replacing netflix_titles.csv
4. Re-run 01_eda.py - no code changes needed, columns match exactly.
"""
import random
import csv
from datetime import datetime

random.seed(42)

genres_pool = [
    "Dramas", "Comedies", "Documentaries", "Action & Adventure",
    "International TV Shows", "Crime TV Shows", "Romantic Movies",
    "Thrillers", "Kids' TV", "Anime Series", "Horror Movies",
    "Stand-Up Comedy", "Sci-Fi & Fantasy", "Reality TV", "Sports Movies",
]

countries_pool = [
    "United States", "India", "United Kingdom", "Canada", "France",
    "Japan", "South Korea", "Spain", "Germany", "Brazil", "Mexico",
    "Australia", "Nigeria", None, None,
]

directors_pool = [
    "Rajiv Mehta", "Susan Carter", "Kenji Watanabe", "Maria Gonzalez",
    "Tom Bennett", "Aisha Khan", "David Lee", "Elena Petrova",
    None, None, None,  # many real entries have missing director
]

ratings_pool = ["TV-MA", "TV-14", "TV-PG", "R", "PG-13", "PG", "TV-Y", "TV-G", "NR"]

first_words = ["The", "A", "Last", "Beyond", "Secret", "Midnight", "Broken", "Golden",
               "Silent", "Hidden", "Eternal", "Lost", "Forgotten", "Rising", "Final"]
second_words = ["Kingdom", "Story", "Journey", "Legacy", "Shadow", "Dream", "Truth",
                "Game", "City", "Heart", "Storm", "Code", "Garden", "Empire", "Echo"]

rows = []
show_id = 1
for _ in range(1200):
    content_type = random.choices(["Movie", "TV Show"], weights=[0.69, 0.31])[0]
    title = f"{random.choice(first_words)} {random.choice(second_words)}"
    director = random.choice(directors_pool) if content_type == "Movie" else None
    cast_size = random.randint(2, 6)
    cast = ", ".join([f"Actor {random.randint(1, 300)}" for _ in range(cast_size)])
    country = random.choice(countries_pool)

    release_year = random.choices(
        population=list(range(2008, 2022)),
        weights=[1, 1, 2, 2, 3, 4, 5, 7, 9, 11, 13, 15, 17, 10],
    )[0]

    added_year = min(release_year + random.randint(0, 4), 2021)
    added_month = random.choice(["January", "February", "March", "April", "May", "June",
                                  "July", "August", "September", "October", "November", "December"])
    added_day = random.randint(1, 28)
    date_added = f"{added_month} {added_day}, {added_year}"

    rating = random.choice(ratings_pool)

    if content_type == "Movie":
        duration = f"{random.randint(60, 180)} min"
    else:
        duration = f"{random.randint(1, 9)} Season{'s' if random.randint(1,9) > 1 else ''}"

    n_genres = random.randint(1, 3)
    listed_in = ", ".join(random.sample(genres_pool, n_genres))

    description = f"A {random.choice(['gripping','heartwarming','thrilling','quirky','dark'])} tale about {random.choice(['family','revenge','love','survival','ambition'])}."

    rows.append([
        f"s{show_id}", content_type, title, director, cast, country,
        date_added, release_year, rating, duration, listed_in, description
    ])
    show_id += 1

with open("netflix_titles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["show_id", "type", "title", "director", "cast", "country",
                      "date_added", "release_year", "rating", "duration",
                      "listed_in", "description"])
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> netflix_titles.csv")
