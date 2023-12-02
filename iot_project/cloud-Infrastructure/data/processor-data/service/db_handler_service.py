import mysql.connector
from datetime import datetime
import json
import time
import logging

logging.basicConfig(level=logging.INFO)


class DatabaseHandlerService:

    def __init__(self):
        self.connection_params = {
            'host': '172.100.10.18',
            'user': 'admin',
            'password': 'admin',
            'database': 'mysql',
        }
        self.is_db_connected = False
        self.connection = None
        self.cursor = None

    def save(self, json_payload, activity):
        if self.validate_connection():
            insert_query = '''
            INSERT INTO movement
                (date, time, activity, acceleration_x, acceleration_y, acceleration_z, gyro_x, gyro_y, gyro_z)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            values = self.build_movement_params(json_payload, activity)
            try:
                self.cursor.execute(insert_query, values)
                self.connection.commit()
                return True
            except mysql.connector.Error as err:
                logging.error(f"Error executing SQL query: {err}")
        return False

    def build_movement_params(self, json_payload, activity):
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        payload = json.loads(json_payload)[1]
        return (
            current_date,
            current_time,
            activity,
            payload.get("acceleration_x", 0),
            payload.get("acceleration_y", 0),
            payload.get("acceleration_z", 0),
            payload.get("gyro_x", 0),
            payload.get("gyro_y", 0),
            payload.get("gyro_z", 0)
        )


    def validate_user_password(self, username, password):
        error = None
        if self.validate_connection():
            select_query = '''
                SELECT id FROM users
                WHERE username = %s AND password = %s
            '''
            values = (username, password)
            try:
                self.cursor.execute(select_query, values)
                result = self.cursor.fetchone()
                return {"isDbConnected": self.is_db_connected, "result": result}
            except mysql.connector.Error as err:
                error = {"error": err}
            finally:
                self.close_connection()
        return error

    def health(self):
        error = None
        if self.validate_connection():
            select_query = "SELECT * FROM users"
            try:
                self.cursor.execute(select_query)
                result = self.cursor.fetchone()
                return {"isDbConnected": self.is_db_connected, "result": result[1]}
            except mysql.connector.Error as err:
                error = err
                logging.error(f"Error executing SQL query: {err}")
            finally:
                self.close_connection()
        return error

    def open_connection(self):
        start_time = time.time()
        while not self.is_db_connected and time.time() - start_time < 10:
            try:
                self.connection = mysql.connector.connect(**self.connection_params)
                self.cursor = self.connection.cursor()
                self.is_db_connected = True
                return True
            except mysql.connector.Error as err:
                logging.info(f"Database connection failed: {err}")
                time.sleep(1)
        return self.is_db_connected

    def validate_connection(self):
        if not self.is_db_connected:
            return self.open_connection()
        return True

    def close_connection(self):
        if self.is_db_connected and self.cursor is not None:
            self.cursor.close()
            self.connection.close()
            self.is_db_connected = False

    def __del__(self):
        if self.is_db_connected and self.cursor is not None:
            self.cursor.close()
            self.connection.close()
            self.is_db_connected = False


if __name__ == '__main__':
    c = DatabaseHandlerService()
    val = c.health()
    print(val)