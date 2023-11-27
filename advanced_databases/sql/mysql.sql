
# 3a
SELECT salary_id, max_salary FROM salaries;

SELECT company_id, location FROM job_postings;

# 3b
SELECT count(*) FROM job_postings jp
    LEFT JOIN companies c on jp.company_id = c.company_id
    WHERE jp.title LIKE '%er';

SELECT avg(jp.max_salary), min(jp.max_salary), max(jp.max_salary) FROM salaries s
    RIGHT JOIN job_postings jp on s.job_id = jp.job_id
    WHERE jp.max_salary > 5000;

# 3C
UPDATE benefits SET type = 'test' WHERE type = 'Medical insurance' LIMIT 10;

# 3D
INSERT INTO companies
    (company_id, name, description, company_size, state, country, city, zip_code, address, url)
VALUES
    (1, 'Empresas Empresas', 'Fazemos tudo e mais alguma coisa', 15, 'CA', 'USA', 'Los Angeles', '2625-136', 'Rua 29 de Fevereiro', 'https://www.example.com');

SELECT * FROM companies WHERE company_id = 1;

