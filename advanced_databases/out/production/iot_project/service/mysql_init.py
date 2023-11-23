import os
import numpy as np
import pandas as pd
import mysql.connector
import threading


# files = ["companies", "job_postings", "employee_counts", "benefits", "salaries"]
files = ["job_postings"]
client = mysql.connector.connect(user='admin', password='admin', host='localhost', port=3306, database='mysql')
mycursor = client.cursor()



def insert_row(query, chunk, table, row_index):
    try:
        mycursor.executemany(query, [tuple(c) for c in chunk])
        client.commit()
        print(f'Inserted smaller chunk: on table {table}. Ids: {[tuple(var)[0] for var in chunk]}')
    except Exception as err:
        print(f'Error inserting chunk on table {table}, error: {err}')
        return False
    return True


def insert_smaller_chunks(data_tuples):
    chunk_index = 0
    new_chunk = np.array_split(data_tuples, len(data_tuples) / 50)
    for chunk in new_chunk:
        insert_row(insert_query, chunk, f, chunk_index)
        chunk_index += 1


for f in files:
    file_path = os.path.join(os.path.dirname(__file__), '../', 'utils', f'{f}.csv')
    data = pd.read_csv(file_path, encoding='utf-8')
    data = data.fillna(0)

    id_columns = [col for col in data.columns if col.lower().endswith('pany_id')]
    data[id_columns] = data[id_columns].astype(int)
    array_chunks = np.array_split(data.values, len(data.values) / 500)

    values = ', '.join(['%s'] * len(data.columns))
    insert_query = f"INSERT INTO {f} VALUES ({values})"

    for chunk in array_chunks:
        try:
            mycursor.executemany(insert_query, [tuple(c) for c in chunk])
            client.commit()
            print(f'Chunk inserted to {f}. {[tuple(var)[0] for var in chunk]}')
        except:
            insert_smaller_chunks(chunk)

mycursor.close()
client.close()