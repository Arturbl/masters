import pandas as pd
from pymongo import MongoClient
import mysql.connector

tables = ["benefits", "companies", "employee_counts", "job_postings", "salaries"]
mongo_client = MongoClient('mongodb://root:rootpassword@localhost:27017/admin')
mongo_db = mongo_client.admin

mysql_client = mysql.connector.connect(user='admin', password='admin', host='localhost', port=3306, database='mysql')
mysql_cursor = mysql_client.cursor()


def fetch_data_from_mysql(table):
    query = f"SELECT * FROM {table}"
    mysql_cursor.execute(query)
    columns = [column[0] for column in mysql_cursor.description]
    data = mysql_cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    return df


def init():
    for table in tables:
        data_df = fetch_data_from_mysql(table)
        mongo_collection = mongo_db[table]
        data_json = data_df.to_dict(orient='records')
        mongo_collection.insert_many(data_json)
        print(f'Collection created and data added for: {table}')
    mysql_cursor.close()
    mysql_client.close()


if __name__ == '__main__':
    init()

