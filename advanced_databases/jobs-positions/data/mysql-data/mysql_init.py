import pandas as pd
import json
from pymongo import MongoClient

# MongoDB connection parameters
username = 'root'
password = 'rootpassword'
databaseName = 'admin'

client = MongoClient(f'mongodb://{username}:{password}@localhost:27017/{databaseName}')
db = client.admin

files = ["benefits", "companies"]
for f in files:
    file = open(f'../utils/{f}.csv')
    data = pd.read_csv(file)
    collection = db.f
    data_json = data.to_dict(orient='records')
    result = collection.insert_many(data_json)

print(f"Inserted ids: {result.inserted_ids}")
