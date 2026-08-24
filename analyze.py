"""
Task 2 — SQLite/SQL analysis and Matplotlib visualizations.
Run collect_and_prepare.py first.
"""
from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
CSV = BASE / "github_projects.csv"
DB = BASE / "github_projects.db"
FIGURES = BASE / "figures"
FIGURES.mkdir(exist_ok=True)

if not CSV.exists():
    raise FileNotFoundError("github_projects.csv not found. Run collect_and_prepare.py first.")

df = pd.read_csv(CSV)

with sqlite3.connect(DB) as conn:
    df.to_sql("Repositories", conn, if_exists="replace", index=False)

    queries = {
        "more_than_10000_stars": """
            SELECT name, owner, language, stars
            FROM Repositories
            WHERE stars > 10000
            ORDER BY stars DESC;
        """,
        "name_contains_machine": """
            SELECT name, owner, language, stars
            FROM Repositories
            WHERE name LIKE '%Machine%'
            ORDER BY stars DESC;
        """,
        "logical_and": """
            SELECT name, owner, language, stars, forks
            FROM Repositories
            WHERE stars > 10000 AND forks > 1000
            ORDER BY stars DESC;
        """,
        "logical_or": """
            SELECT name, owner, language, stars, forks
            FROM Repositories
            WHERE language = 'Python' OR language = 'Jupyter Notebook'
            ORDER BY stars DESC;
        """,
        "logical_not": """
            SELECT name, owner, language, stars
            FROM Repositories
            WHERE NOT language = 'Unknown'
            ORDER BY stars DESC;
        """,
        "sorted_all": """
            SELECT name, owner, language, stars
            FROM Repositories
            ORDER BY stars DESC;
        """,
        "top_10": """
            SELECT name, owner, language, stars, forks
            FROM Repositories
            ORDER BY stars DESC
            LIMIT 10;
        """,
        "summary": """
            SELECT COUNT(*) AS total_repositories,
                   ROUND(AVG(stars), 2) AS average_stars
            FROM Repositories;
        """,
        "languages_over_5": """
            SELECT language, COUNT(*) AS repository_count,
                   ROUND(AVG(stars), 2) AS average_stars
            FROM Repositories
            GROUP BY language
            HAVING COUNT(*) > 5
            ORDER BY repository_count DESC;
        """,
    }

    results = {}
    for name, sql in queries.items():
        results[name] = pd.read_sql_query(sql, conn)

    with open(BASE / "sql_results.txt", "w", encoding="utf-8") as f:
        for name, result in results.items():
            f.write(f"\n=== {name} ===\n")
            f.write(result.to_string(index=False))
            f.write("\n")

# Visualization 1: Top 10 repositories by stars.
top10 = results["top_10"].copy()
if not top10.empty:
    top10["repo"] = top10["owner"] + "/" + top10["name"]
    plt.figure(figsize=(11, 6))
    plt.barh(top10["repo"].iloc[::-1], top10["stars"].iloc[::-1])
    plt.xlabel("Stars")
    plt.ylabel("Repository")
    plt.title("Top 10 Machine Learning Repositories by GitHub Stars")
    plt.tight_layout()
    plt.savefig(FIGURES / "top_10_repositories.png", dpi=180)
    plt.close()

# Visualization 2: Repository creation trends over time.
df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
trend = (
    df.dropna(subset=["created_date"])
      .assign(year=lambda x: x["created_date"].dt.year)
      .groupby("year")
      .size()
)
if not trend.empty:
    plt.figure(figsize=(10, 5))
    plt.plot(trend.index, trend.values, marker="o")
    plt.xlabel("Year")
    plt.ylabel("Number of repositories")
    plt.title("Machine Learning Repository Creation Trend")
    plt.tight_layout()
    plt.savefig(FIGURES / "repository_creation_trend.png", dpi=180)
    plt.close()

print("Analysis complete.")
print(f"Database: {DB}")
print(f"Results: {BASE / 'sql_results.txt'}")
print(f"Figures: {FIGURES}")
