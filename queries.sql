-- Task 2 SQL requirements

-- 1. Repositories with more than 10,000 stars
SELECT name, owner, language, stars
FROM Repositories
WHERE stars > 10000
ORDER BY stars DESC;

-- 2. Repository names containing "Machine"
SELECT name, owner, language, stars
FROM Repositories
WHERE name LIKE '%Machine%'
ORDER BY stars DESC;

-- 3. AND
SELECT name, owner, language, stars, forks
FROM Repositories
WHERE stars > 10000 AND forks > 1000
ORDER BY stars DESC;

-- 4. OR
SELECT name, owner, language, stars
FROM Repositories
WHERE language = 'Python' OR language = 'Jupyter Notebook'
ORDER BY stars DESC;

-- 5. NOT
SELECT name, owner, language, stars
FROM Repositories
WHERE NOT language = 'Unknown'
ORDER BY stars DESC;

-- 6. Sort by stars
SELECT name, owner, language, stars
FROM Repositories
ORDER BY stars DESC;

-- 7. Top 10
SELECT name, owner, language, stars, forks
FROM Repositories
ORDER BY stars DESC
LIMIT 10;

-- 8. Total repositories and average stars
SELECT COUNT(*) AS total_repositories,
       ROUND(AVG(stars), 2) AS average_stars
FROM Repositories;

-- 9. Languages with more than 5 repositories
SELECT language,
       COUNT(*) AS repository_count,
       ROUND(AVG(stars), 2) AS average_stars
FROM Repositories
GROUP BY language
HAVING COUNT(*) > 5
ORDER BY repository_count DESC;
