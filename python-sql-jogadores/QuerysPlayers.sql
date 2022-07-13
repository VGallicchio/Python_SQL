--Qual posição mais paga por estado?
SELECT t.team_state, p.position, salary
		FROM (
			SELECT p.id, p.position, (s.salary_amount::money) as salary,
			ROW_NUMBER() OVER (PARTITION BY t.team_state ORDER BY s.salary_amount DESC) AS rn
			FROM players p
			JOIN salary s
			ON p.id = s.id_player
			JOIN teams t
			ON t.id = p.team_id
		)AS sub
JOIN players p
ON p.id = sub.id
JOIN teams t
ON t.id = p.team_id
AND sub.rn = 1;

--Média, mínimo e máximo salário por altura?
SELECT DISTINCT p.height AS height,
	AVG(s.salary_amount) OVER salary_by_height AS avg_salary,
	MIN(s.salary_amount) OVER salary_by_height AS min_salary,
	MAX(s.salary_amount) OVER salary_by_height AS max_salary
FROM players p
JOIN salary s
ON s.id_player = p.id
WINDOW salary_by_height AS (PARTITION BY p.height ORDER BY p.height DESC)
ORDER BY 1 DESC;
