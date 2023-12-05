import json
import logging
import time
import mysql.connector
import pandas as pd

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

    def save_data_frame(self, data_frame):
        if self.validate_connection():
            try:
                data_frame['datetime'] = pd.to_datetime(data_frame['datetime'], format='%d-%m-%Y %H:%M:%S')
                rows = [tuple(row) for _, row in data_frame.iterrows()]
                insert_query = '''
                INSERT INTO movement
                    (activity, acceleration_x, acceleration_y, acceleration_z, gyro_x, gyro_y, gyro_z, datetime)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s)
                '''
                self.cursor.executemany(insert_query, rows)
                self.connection.commit()
            except Exception as e:
                print(f"Could not insert training data. Error: {e}")
            finally:
                self.close_connection()
            return True
        return False


    def save(self, json_payload, activity):
        if self.validate_connection():
            insert_query = '''
            INSERT INTO movement
                (activity, acceleration_x, acceleration_y, acceleration_z, gyro_x, gyro_y, gyro_z)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s)
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
        payload = json.loads(json_payload)[1]
        return (
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
                if result:
                    return True
                return False

            except mysql.connector.Error as err:
                error = {"error": err}
            finally:
                self.close_connection()
        return error

    def get_history(self, date_begin, date_end):
        if self.validate_connection():
            query = '''
                SELECT *
                FROM (
                     SELECT * FROM movement
                     WHERE
                         ((datetime >= %s AND datetime < %s) OR
                         date(datetime) = date(%s))
                 ) AS subquery
            '''
            values = (date_begin, date_end, date_begin)
            try:
                self.cursor.execute(query, values)
                result = self.cursor.fetchall()
                if result:
                    return result
                return None
            except mysql.connector.Error as err:
                return None
            finally:
                self.close_connection()

    def get_user_data(self):
        if self.validate_connection():
            query = '''
            SELECT * FROM users 
            '''
            try:
                self.cursor.execute(query)
                result = self.cursor.fetchone()
                if result:
                    return result
                return None
            except mysql.connector.Error as err:
                return None
            finally:
                self.close_connection()

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

    def await_connection(self):
        while not self.is_db_connected:
            try:
                self.connection = mysql.connector.connect(**self.connection_params)
                self.cursor = self.connection.cursor()
                self.is_db_connected = True
                return True
            except mysql.connector.Error as err:
                logging.info(f"Database connection failed: {err}")
                time.sleep(3)
        return self.is_db_connected

    def validate_connection(self):
        if not self.is_db_connected:
            return self.await_connection()
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