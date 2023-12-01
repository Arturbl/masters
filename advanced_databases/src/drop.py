import mysql.connector
from pymongo import MongoClient

MYSQL_CONFIG = {
    'user': 'admin',
    'password': 'admin',
    'host': 'localhost',
    'port': 3306,
    'database': 'mysql'
}

MONGO_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'username': 'root',
    'password': 'rootpassword',
    'authSource': 'admin'
}


def disable_foreign_keys(cursor):
    cursor.execute("SET foreign_key_checks = 0")


def enable_foreign_keys(cursor):
    cursor.execute("SET foreign_key_checks = 1")


def truncate_mysql_tables():
    print("Truncating MySQL tables...")

    mysql_client = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = mysql_client.cursor()

    try:
        disable_foreign_keys(cursor)

        tables = ["benefits", "salaries", "employee_counts", "job_postings", "companies"]

        for table in tables:
            query = f"TRUNCATE TABLE {table}"
            cursor.execute(query)

    finally:
        enable_foreign_keys(cursor)
        mysql_client.commit()
        cursor.close()
        mysql_client.close()


def drop_mongo_collections():
    print("Dropping MongoDB collections...")
    collections = ["benefits", "salaries", "employee_counts", "job_postings", "companies"]

    mongo_client = MongoClient(f"mongodb://{MONGO_CONFIG['username']}:{MONGO_CONFIG['password']}@{MONGO_CONFIG['host']}:{MONGO_CONFIG['port']}/{MONGO_CONFIG['authSource']}")

    for collection in collections:
        db = mongo_client[MONGO_CONFIG['authSource']]
        db[collection].drop()

    mongo_client.close()


if __name__ == "__main__":
    truncate_mysql_tables()
    drop_mongo_collections()
    print("Tables and collections truncated/dropped successfully.")
