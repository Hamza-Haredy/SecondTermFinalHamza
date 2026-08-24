"""
Task 1 — Collect and prepare GitHub repository data.

The script follows the assignment's supplied endpoint:
https://api.github.com/search/repositories?q=machine+learning&sort=stars&order=desc&per_page=100

Optional authentication:
    Set GITHUB_TOKEN in your environment before running.

Output:
    raw_response.json
    github_projects.csv
"""
import json
import os
from pathlib import Path

import pandas as pd
import requests

URL = "https://api.github.com/search/repositories"
PARAMS = {
    "q": "machine learning",
    "sort": "stars",
    "order": "desc",
    "per_page": 100,
}
OUTPUT_DIR = Path(__file__).resolve().parent
RAW_FILE = OUTPUT_DIR / "raw_response.json"
CSV_FILE = OUTPUT_DIR / "github_projects.csv"

headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2026-03-10",
    "User-Agent": "github-ml-data-analytics-project",
}
token = os.getenv("GITHUB_TOKEN")
if token:
    headers["Authorization"] = f"Bearer {token}"

response = requests.get(URL, params=PARAMS, headers=headers, timeout=30)
response.raise_for_status()
data = response.json()
RAW_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

items = data.get("items", [])
if not items:
    raise RuntimeError("GitHub returned no repository items.")

df = pd.DataFrame(items)

required = [
    "name", "owner", "language", "stargazers_count", "forks_count",
    "watchers_count", "open_issues_count", "created_at", "updated_at",
    "license"
]
missing_columns = [c for c in required if c not in df.columns]
if missing_columns:
    raise RuntimeError(f"Missing required columns: {missing_columns}")

df = df[required].copy()

# Extract values from nested objects.
df["owner"] = df["owner"].apply(
    lambda x: x.get("login") if isinstance(x, dict) else x
)
df["license"] = df["license"].apply(
    lambda x: x.get("spdx_id") if isinstance(x, dict) else x
)

# Handle missing values.
df["language"] = df["language"].fillna("Unknown")
df["license"] = df["license"].fillna("No License")

# Remove exact duplicate repository records.
df = df.drop_duplicates(subset=["owner", "name"]).copy()

# Convert dates.
df["created_date"] = pd.to_datetime(df["created_at"], errors="coerce").dt.strftime("%Y-%m-%d")
df["updated_date"] = pd.to_datetime(df["updated_at"], errors="coerce").dt.strftime("%Y-%m-%d")

# Rename required numeric fields.
df = df.rename(columns={
    "stargazers_count": "stars",
    "forks_count": "forks",
    "watchers_count": "watchers",
    "open_issues_count": "open_issues",
})

# Keep the assignment's final analytical fields.
df = df[
    ["name", "owner", "language", "stars", "forks", "watchers",
     "open_issues", "created_date", "updated_date", "license"]
].copy()

df.to_csv(CSV_FILE, index=False)

# Verification.
check = pd.read_csv(CSV_FILE)
print(f"Repositories collected: {len(check)}")
print(f"Columns: {list(check.columns)}")
print(f"Duplicate rows: {check.duplicated().sum()}")
print(f"Missing values by column:\n{check.isna().sum()}")
print(f"Saved: {CSV_FILE}")
