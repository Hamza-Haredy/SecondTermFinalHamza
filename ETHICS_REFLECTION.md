# Ethics Reflection

## 1. Why is it important to verify data collected from public APIs?

Public API data can change over time and may contain missing, unexpected, or inconsistent values. Verification helps confirm that the response was received successfully, that the required fields are present, and that the dataset has been cleaned correctly before analysis. This reduces the risk of producing inaccurate results.

## 2. Why should data analysts document the source of their data?

Documenting the source makes the analysis transparent and reproducible. Other people can understand where the data came from, repeat the collection process, and evaluate whether the source is appropriate for the business question. In this project, the GitHub API endpoint and collection process are documented in the code and README.

## 3. How can missing or inaccurate data affect data analysis and decision-making?

Missing or inaccurate data can distort summary statistics, rankings, comparisons, and trends. For example, missing programming-language values could make language-based analysis misleading, while incorrect star counts could change the ranking of popular repositories. Analysts should identify and appropriately handle these issues before drawing conclusions.
