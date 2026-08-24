# GitHub Machine Learning Repository Analytics

## Project overview

This project analyzes Machine Learning repositories returned by the GitHub Search API. It follows the assignment workflow:

1. Collect repository data from the GitHub API.
2. Prepare and clean the JSON data using Python and Pandas.
3. Save the cleaned dataset as `github_projects.csv`.
4. Store the dataset in SQLite.
5. Analyze the data using SQL.
6. Create Matplotlib visualizations.
7. Interpret the findings.
8. Manage the project with Git and publish it on GitHub.
9. Complete an ethics reflection.

## Data source

The assignment supplies this endpoint:

`https://api.github.com/search/repositories?q=machine+learning&sort=stars&order=desc&per_page=100`

The script uses the same search parameters.

## Files

- `collect_and_prepare.py` — API collection and Pandas preparation.
- `analyze.py` — SQLite loading, SQL analysis, and visualizations.
- `queries.sql` — required SQL queries.
- `github_projects.csv` — generated cleaned dataset.
- `github_projects.db` — generated SQLite database.
- `figures/` — generated charts.
- `sql_results.txt` — generated SQL output.
- `raw_response.json` — raw API response.
- `requirements.txt` — Python dependencies.

## How to run

```bash
python -m pip install -r requirements.txt
python collect_and_prepare.py
python analyze.py
```

If GitHub rate limits are reached, authenticate with a personal access token stored in the `GITHUB_TOKEN` environment variable. Do not put the token directly in the source code.

## Analysis requirements completed

- More than 10,000 stars
- Names containing "Machine"
- AND, OR, and NOT
- Sorting by stars
- Top 10 repositories
- Repository count
- Average stars
- GROUP BY language
- HAVING more than 5 repositories
- Popularity visualization
- Creation-trend visualization

## Responsible data use

The API data is public, but it should still be treated carefully. The collection date and endpoint should be documented because repository statistics can change. Missing values and API errors should be handled rather than silently ignored. Findings should describe what is present in the collected sample and should not be generalized beyond that dataset without additional evidence.
