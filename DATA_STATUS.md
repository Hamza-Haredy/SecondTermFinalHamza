# Data status

The assignment requires `github_projects.csv` to be generated from the live GitHub API.
This workspace cannot directly execute the external API request, so no fabricated repository
records are included. Run `python collect_and_prepare.py` on a machine with internet access
to create the real dataset, then run `python analyze.py`.
