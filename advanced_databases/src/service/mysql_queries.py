import os

import mysql.connector
import numpy as np
import pandas as pd
import time

client = mysql.connector.connect(user='admin', password='admin', host='localhost', port=3306, database='mysql')
mycursor = client.cursor()

x = 10
times = []

for i in range(x):
    time_i = time.time()
    mycursor.execute("SELECT salary_id, AVG(max_salary) AS avg_max_salary "
                     "FROM salaries GROUP BY salary_id ORDER BY avg_max_salary DESC")
    myresult1 = mycursor.fetchall()
    time_f = time.time()
    times.append(time_f-time_i)

avgtime = sum(times)/x
print('No optimization:  avg total time SQL-Query 3a-1 = ', avgtime)
times = []

for i in range(x):

    time_i = time.time()
    mycursor.execute("WITH ranked_postings AS ("
                     "SELECT company_id, location, ROW_NUMBER() OVER (PARTITION BY location ORDER BY COUNT(*) DESC) AS posting_rank "
                     "FROM job_postings GROUP BY company_id, location)"
                     "SELECT company_id, location FROM ranked_postings WHERE posting_rank = 1;")
    myresult2 = mycursor.fetchall()
    time_f = time.time()
    times.append(time_f-time_i)

avgtime = sum(times)/x
print('No optimization: avg total time SQL-Query 3a-2 = ', avgtime)
times = []


for i in range(x):
    time_i = time.time()
    mycursor.execute("SELECT c.company_id, c.name as company_name, ec.employee_count, COUNT(*) as job_count "
                     "FROM job_postings jp "
                     "LEFT JOIN companies c ON jp.company_id = c.company_id "
                     "LEFT JOIN benefits b ON jp.job_id = b.job_id "
                     "LEFT JOIN employee_counts ec ON c.company_id = ec.company_id "
                     "WHERE jp.title LIKE '%er' GROUP BY c.company_id, c.name, ec.employee_count "
                     "HAVING job_count > 5 ORDER BY job_count DESC;")

    myresult3 = mycursor.fetchall()
    time_f = time.time()
    times.append(time_f-time_i)

avgtime = sum(times)/x
print('No optimization: avg total time SQL-Query 3b-1 = ', avgtime)
times = []


for i in range(x):
    time_i = time.time()
    mycursor.execute("SELECT avg(jp.max_salary), min(jp.max_salary), max(jp.max_salary) FROM salaries s "
                     "RIGHT JOIN job_postings jp on s.job_id = jp.job_id "
                     "WHERE jp.max_salary > 5000;")
    myresult4 = mycursor.fetchall()
    time_f = time.time()
    times.append(time_f-time_i)

avgtime = sum(times)/x
print('No optimization: avg total time SQL-Query 3b-2 = ',avgtime )
times = []