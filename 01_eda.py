"""
Netflix Catalog EDA
===================
A beginner-to-intermediate exploratory data analysis project on Netflix's
content catalog (movies & TV shows).

Dataset structure matches: https://www.kaggle.com/datasets/shivamb/netflix-shows
(see generate_data.py docstring for how to swap in the real CSV)

Sections:
1. Load & inspect
2. Clean
3. Analysis + visualizations
4. Save findings
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110

# -----------------------------------------------------------------------
# 1. LOAD & INSPECT
# -----------------------------------------------------------------------
df = pd.read_csv("netflix_titles.csv")

print("=" * 60)
print("SHAPE:", df.shape)
print("=" * 60)
print("\nCOLUMN INFO:")
print(df.info())

print("\nMISSING VALUES PER COLUMN:")
print(df.isnull().sum())

print("\nFIRST 5 ROWS:")
print(df.head())

# -----------------------------------------------------------------------
# 2. CLEAN
# -----------------------------------------------------------------------
# director/cast/country can be legitimately missing (Netflix metadata gaps) -
# fill with 'Unknown' rather than dropping rows, since dropping would
# throw away otherwise-good data in other columns.
df["director"] = df["director"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")

# date_added -> proper datetime so we can extract year/month
df["date_added"] = pd.to_datetime(df["date_added"], format="%B %d, %Y", errors="coerce")
df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month_name()

# duration: split movies (minutes) from TV shows (seasons) into separate
# numeric columns since they're not comparable units
df["duration_value"] = df["duration"].str.extract(r"(\d+)").astype(float)

print("\nDuplicate rows:", df.duplicated().sum())
print("Cleaned. Shape now:", df.shape)

# listed_in has comma-separated multiple genres per title - explode into
# one row per (title, genre) pair for genre-level analysis
df["genre_list"] = df["listed_in"].str.split(", ")
genres_exploded = df.explode("genre_list")

# -----------------------------------------------------------------------
# 3. ANALYSIS + VISUALIZATIONS
# -----------------------------------------------------------------------

# --- 3a. Movies vs TV Shows split ---
type_counts = df["type"].value_counts()
print("\nContent type breakdown:\n", type_counts)

fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(type_counts.values, labels=type_counts.index, autopct="%1.1f%%",
       colors=["#E50914", "#221F1F"], startangle=90,
       labeldistance=1.1, pctdistance=0.7,
       textprops={"fontweight": "bold"},
       wedgeprops={"edgecolor": "white", "linewidth": 1.5})
for autotext in ax.texts:
    if "%" in autotext.get_text():
        autotext.set_color("white")
ax.set_title("Movies vs TV Shows on Netflix", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("chart1_type_split.png", facecolor="white")
plt.close()

# --- 3b. Titles added per year ---
yearly = df["year_added"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(yearly.index.astype(int).astype(str), yearly.values, color="#E50914")
ax.set_title("Titles Added to Netflix per Year", fontsize=13, fontweight="bold")
ax.set_xlabel("Year Added")
ax.set_ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart2_titles_per_year.png", facecolor="white")
plt.close()

# --- 3c. Top 10 genres ---
top_genres = genres_exploded["genre_list"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(top_genres.index[::-1], top_genres.values[::-1], color="#221F1F")
ax.set_title("Top 10 Genres on Netflix", fontsize=13, fontweight="bold")
ax.set_xlabel("Number of Titles")
plt.tight_layout()
plt.savefig("chart3_top_genres.png", facecolor="white")
plt.close()

# --- 3d. Top 10 countries producing content ---
top_countries = df[df["country"] != "Unknown"]["country"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(top_countries.index[::-1], top_countries.values[::-1], color="#E50914")
ax.set_title("Top 10 Content-Producing Countries", fontsize=13, fontweight="bold")
ax.set_xlabel("Number of Titles")
plt.tight_layout()
plt.savefig("chart4_top_countries.png", facecolor="white")
plt.close()

# --- 3e. Movie duration distribution ---
movie_durations = df[df["type"] == "Movie"]["duration_value"]

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(movie_durations, bins=20, color="#E50914", edgecolor="white")
ax.axvline(movie_durations.mean(), color="black", linestyle="--", linewidth=2,
           label=f"Mean: {movie_durations.mean():.0f} min")
ax.set_title("Distribution of Movie Durations", fontsize=13, fontweight="bold")
ax.set_xlabel("Duration (minutes)")
ax.set_ylabel("Count")
ax.legend()
plt.tight_layout()
plt.savefig("chart5_movie_durations.png", facecolor="white")
plt.close()

# -----------------------------------------------------------------------
# 4. SAVE FINDINGS
# -----------------------------------------------------------------------
findings = f"""
NETFLIX CATALOG EDA — KEY FINDINGS
===================================

Dataset: {df.shape[0]} titles, {df.shape[1]} original columns

1. CONTENT MIX
   - Movies: {type_counts.get('Movie', 0)} ({type_counts.get('Movie', 0)/len(df)*100:.1f}%)
   - TV Shows: {type_counts.get('TV Show', 0)} ({type_counts.get('TV Show', 0)/len(df)*100:.1f}%)
   - Movies dominate the catalog by roughly a 2:1 ratio.

2. GROWTH OVER TIME
   - Titles added peaked around {int(yearly.idxmax())} ({int(yearly.max())} titles that year),
     suggesting aggressive catalog expansion in that period.

3. TOP GENRES
   - Most common genre: {top_genres.index[0]} ({top_genres.iloc[0]} titles)
   - Genres are heavily skewed toward Dramas, Comedies, and Documentaries.

4. CONTENT ORIGIN
   - Top producing country: {top_countries.index[0]} ({top_countries.iloc[0]} titles)
   - A large share of content is concentrated in a handful of countries.

5. MOVIE LENGTH
   - Average movie duration: {movie_durations.mean():.0f} minutes
   - Most movies cluster between {movie_durations.quantile(0.25):.0f} and
     {movie_durations.quantile(0.75):.0f} minutes (interquartile range).

6. DATA QUALITY NOTES
   - 'director' and 'country' had missing values, filled with 'Unknown'
     rather than dropped, to avoid losing valid data in other columns.
   - 'listed_in' contains multiple comma-separated genres per title;
     exploded into one row per genre for accurate genre-level counts.
"""

with open("findings.txt", "w") as f:
    f.write(findings)

print(findings)
print("\nAll charts saved as PNG files. Findings saved to findings.txt")
