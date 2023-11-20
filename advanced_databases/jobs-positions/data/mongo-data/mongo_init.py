import pandas as pd
from pymongo import MongoClient

username = 'root'
password = 'rootpassword'
databaseName = 'admin'

client = MongoClient(f'mongodb://{username}:{password}@localhost:27017/{databaseName}')
db = client.admin

files = ["benefits", "companies", "employee_counts", "job_postings", "salaries"]

for f in files:
    file_path = f'../utils/{f}.csv'
    data = pd.read_csv(file_path, encoding='utf-8')
    collection = db[f]
    data_json = data.to_dict(orient='records')
    result = collection.insert_many(data_json)

print(f"Inserted ids: {result.inserted_ids}")
