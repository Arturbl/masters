import pandas as pd
from pymongo import MongoClient
import time


mongo_client = MongoClient('mongodb://root:rootpassword@localhost:27017/admin')
db = mongo_client.admin

print("hello")

