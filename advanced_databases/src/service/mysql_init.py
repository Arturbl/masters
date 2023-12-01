import os

import mysql.connector
import numpy as np
import pandas as pd


files = ["companies", "job_postings", "employee_counts", "benefits", "salaries"]
client = mysql.connector.connect(user='admin', password='admin', host='localhost', port=3306, database='mysql')
mycursor = client.cursor()


def insert_row(query, chunk, f, row_index, data_frame):
    try:
        data_tuples = [tuple(c) for c in chunk]
        mycursor.executemany(query, data_tuples)
        client.commit()
        print(f'{f.upper()} Inserting smaller chunk with ids: {[tuple(c)[0] for c in chunk]}')
    except Exception as err:
        print(f'{f.upper()} Error inserting chunk: {err}')
        # delete_rows_from_csv(f, data_frame, row_index, len(chunk))
        return False
    return True


# def delete_rows_from_csv(f, data_frame, start_index, num_rows):
#     data_frame.drop(data_frame.index[start_index:start_index + num_rows], inplace=True)
#     data_frame.to_csv(f, index=False, encoding='utf-8')


def insert_smaller_chunks(insert_query, f, data_tuples, data_frame):
    chunk_index = 0
    new_chunk = np.array_split(data_tuples, len(data_tuples) / 50)
    for chunk in new_chunk:
        insert_row(insert_query, chunk, f, chunk_index, data_frame)
        chunk_index += 1


def init():
    for f in files:
        file_path = os.path.join(os.path.dirname(__file__), '../', 'utils', f'{f}.csv')
        data_frame = pd.read_csv(file_path, encoding='utf-8')
        data_frame = data_frame.fillna(0)

        # id_columns = [col for col in data_frame.columns if col.lower().endswith('pany_id')]
        # data_frame[id_columns] = data_frame[id_columns].astype(int)
        array_chunks = np.array_split(data_frame.values, len(data_frame.values) / 500)

        values = ', '.join(['%s'] * len(data_frame.columns))
        insert_query = f"INSERT INTO {f} VALUES ({values})"

        for chunk in array_chunks:
            try:
                mycursor.executemany(insert_query, [tuple(c) for c in chunk])
                client.commit()
                print(f'{f.upper()} Inserting smaller chunk with ids: {[tuple(var)[0] for var in chunk]}')
            except:
                insert_smaller_chunks(insert_query, f, chunk, data_frame)

    mycursor.close()
    client.close()


if __name__ == '__main__':
    init()