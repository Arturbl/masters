import os
import pandas as pd
from pymongo import MongoClient


files = ["benefits", "companies", "employee_counts", "job_postings", "salaries"]
client = MongoClient('mongodb://root:rootpassword@localhost:27017/admin')
db = client.admin


def init():
    for f in files:
        file_path = os.path.join(os.path.dirname(__file__), '../', 'utils', f'{f}.csv')
        data = pd.read_csv(file_path, encoding='utf-8')
        collection = db[f]
        data_json = data.to_dict(orient='records')
        collection.insert_many(data_json)
        print(f'Collection created: {f}')


init()