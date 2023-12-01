import mysql.connector
from pymongo import MongoClient

files = ["benefits", "salaries", "employee_counts", "job_postings", "companies"]


def disable_foreign_keys(cursor):
    cursor.execute("SET foreign_key_checks = 0")


def enable_foreign_keys(cursor):
    cursor.execute("SET foreign_key_checks = 1")


def truncate_mysql_tables():
    print("Truncating MySQL tables...")
    mysql_client = mysql.connector.connect(user='admin', password='admin', host='localhost', port=3306, database='mysql')
    cursor = mysql_client.cursor()
    try:
        disable_foreign_keys(cursor)
        for table in files:
            query = f"TRUNCATE TABLE {table}"
            cursor.execute(query)
    finally:
        enable_foreign_keys(cursor)
        mysql_client.commit()
        cursor.close()
        mysql_client.close()


def drop_mongo_collections():
    print("Dropping MongoDB collections...")
    mongo_client = MongoClient('mongodb://root:rootpassword@localhost:27017/admin')
    for collection in files:
        db = mongo_client.admin
        db[collection].drop()
    mongo_client.close()


if __name__ == "__main__":
    truncate_mysql_tables()
    drop_mongo_collections()
    print("Tables and collections truncated/dropped successfully.")
