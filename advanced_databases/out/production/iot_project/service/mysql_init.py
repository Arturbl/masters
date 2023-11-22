import os
import pandas as pd
import mysql.connector
import numpy as np

client = mysql.connector.connect(
    user='admin',
    password='admin',
    host='localhost',
    port=3306,
    database='mysql'
)

mycursor = client.cursor()

files = ["companies", "job_postings", "employee_counts", "benefits", "salaries"]


for f in files:
    file_path = os.path.join(os.path.dirname(__file__), '../', 'utils', f'{f}.csv')
    data = pd.read_csv(file_path, encoding='utf-8')
    data = data.fillna(0)

    data_tuples = [tuple(row) for row in data.values]

    values = ', '.join(['%s'] * len(data.columns))
    insert_query = f"INSERT INTO {f} VALUES ({values})"

    mycursor.executemany(insert_query, data_tuples)

    client.commit()

    print(f"{mycursor.rowcount} records inserted for {f}.")

mycursor.close()
client.close()
