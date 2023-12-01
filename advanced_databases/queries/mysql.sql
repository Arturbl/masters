
# -------------------------------------- 3a -----------------
SELECT salary_id, AVG(max_salary) AS avg_max_salary
FROM salaries
GROUP BY salary_id
ORDER BY avg_max_salary DESC;

#Esta consulta calcula o salário máximo médio para cada empresa e, em seguida, ordena os resultados por ordem
# decrescente do salário máximo médio.

WITH ranked_postings AS (
    SELECT
        company_id,
        location,
        ROW_NUMBER() OVER (PARTITION BY location ORDER BY COUNT(*) DESC) AS posting_rank
    FROM job_postings
    GROUP BY company_id, location
)
SELECT company_id, location
FROM ranked_postings
WHERE posting_rank = 1;

#Esta consulta utiliza uma expressão de tabela comum e a função de janela ROW_NUMBER() para classificar as empresas
# com base no número de ofertas de emprego em cada localização. O resultado final inclui apenas as empresas com o
# maior número de ofertas de emprego em cada local.

# -------------------------------------- 3b -----------------
SELECT
    c.company_id,
    c.name as company_name,
    ec.employee_count,
    COUNT(*) as job_count
FROM job_postings jp
         LEFT JOIN companies c ON jp.company_id = c.company_id
         LEFT JOIN benefits b ON jp.job_id = b.job_id
         LEFT JOIN employee_counts ec ON c.company_id = ec.company_id
WHERE jp.title LIKE '%er'
GROUP BY c.company_id, c.name, ec.employee_count
HAVING job_count > 5
ORDER BY job_count DESC;

#Esta consulta recupera informações sobre empresas, incluindo o seu ID, nome, número de empregados e o número de ofertas
# de emprego em que o título contém "er". Também filtra as empresas com mais de 5 ofertas de emprego e ordena os resultados
# pela contagem de ofertas por ordem decrescente. A utilização de LEFT JOINs garante que as empresas sem entradas correspondentes
# nas tabelas benefits ou employee_counts continuam a ser incluídas nos resultados.


SELECT avg(jp.max_salary), min(jp.max_salary), max(jp.max_salary) FROM salaries s
    RIGHT JOIN job_postings jp on s.job_id = jp.job_id
    WHERE jp.max_salary > 5000;

#Essa consulta calcula os valores médio, mínimo e máximo da coluna max_salary da tabela salaries, considerando apenas as
# linhas em que os anúncios de emprego correspondentes têm um max_salary maior que 5000. O RIGHT JOIN garante que todas
# as linhas da tabela job_postings sejam incluídas, e as linhas correspondentes da tabela salaries sejam incluídas com
# valores NULL se não houver correspondência.

# -------------------------------------- 3C -----------------
UPDATE benefits SET type = 'test' WHERE type = 'Medical insurance' LIMIT 10;

#Esta consulta atualiza até 10 linhas na tabela benefits, alterando o valor da coluna type de 'Medical insurance' para 'test'.
# O LIMIT 10 garante que apenas um máximo de 10 linhas sejam atualizadas, mesmo que haja mais linhas que satisfaçam a condição.

# -------------------------------------- 3D -----------------
INSERT INTO companies
    (company_id, name, description, company_size, state, country, city, zip_code, address, url)
VALUES
    (1, 'Empresas Empresas', 'Fazemos tudo e mais alguma coisa', 15, 'CA', 'USA', 'Los Angeles', '2625-136', 'Rua 29 de Fevereiro', 'https://www.example.com');

#----------------------------------------------------------------
