import os
import pandas as pd
import mysql.connector


files = ["companies", "job_postings", "employee_counts", "benefits", "salaries"]
client = mysql.connector.connect(user='admin', password='admin', host='localhost', port=3306, database='mysql')
mycursor = client.cursor()


def insert_row(query, data_tuple, table, row_index):
    try:
        mycursor.execute(query, data_tuple)
        client.commit()
        print(f'Inserted row: {data_tuple[0]} on table {table}. Row index: {row_index}')
    except Exception as err:
        print(f'Error inserting row: {data_tuple[0]} on table {table}, error: {err}')
        return False
    return True


def run_row_by_row():
    global data
    index = 0
    rows_to_delete = []
    for data_tuple in data_tuples:
        success = insert_row(insert_query, data_tuple, f, index)
        if not success:
            rows_to_delete.append(index)
        index += 1
    if rows_to_delete:
        print(f'Deleting rows from {f}.csv:', rows_to_delete)
        data = data.drop(index=rows_to_delete)
        data.to_csv(file_path, index=False, encoding='utf-8')


for f in files:
    file_path = os.path.join(os.path.dirname(__file__), '../', 'utils', f'{f}.csv')
    data = pd.read_csv(file_path, encoding='utf-8')
    data = data.fillna(0)

    data_tuples = [tuple(row) for row in data.values]

    values = ', '.join(['%s'] * len(data.columns))
    insert_query = f"INSERT INTO {f} VALUES ({values})"

    try:
        mycursor.executemany(insert_query, data_tuples)
        client.commit()
        print(f'data inserted to {f}')
    except:
        run_row_by_row()

mycursor.close()
client.close()