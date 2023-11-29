import psycopg2
from datetime import datetime
import time
import logging

logging.basicConfig(level=logging.INFO)


class DatabaseHandlerService:

    def __init__(self):
        self.is_db_connected = False
        self.connection = None
        self.cursor = None

    def save(self, payload, activity):
        print(f"Saving payload {payload} and activity {activity}")
        is_db_connected = self.validate_connection()
        if is_db_connected:
            insert_query = '''
            INSERT INTO movement 
                (date, time, activity, acceleration_x, acceleration_y, acceleration_z, gyro_x, gyro_y, gyro_z)
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            values = self.build_movement_params(payload, activity)
            self.cursor.execute(insert_query, values)
            self.connection.commit()
        return False

    def build_movement_params(self, payload, activity):
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        return (
            current_date,
            current_time,
            activity,
            payload.acceleration_x,
            payload.acceleration_y,
            payload.acceleration_z,
            payload.gyro_x,
            payload.gyro_y,
            payload.gyro_z
        )

    def validate_user_password(self, username, password):
        print(f"Validation username {username} and password {password}")
        is_db_connected = self.validate_connection()
        if is_db_connected:
            select_query = '''
                SELECT id FROM users
                WHERE username = %s AND password = %s
            '''
            values = (username, password)
            self.cursor.execute(select_query, values)
            result = self.cursor.fetchone()
            return result is not None
        return False

    def health(self):
        print("Checking database}")
        is_db_connected = self.validate_connection()
        if is_db_connected:
            select_query = "SELECT * FROM movement"
            self.cursor.execute(select_query)
            result = self.cursor.fetchone()
            return result is not None
        return False

    def open_connection(self):
        index = 0
        while not self.is_db_connected and index < 11:
            try:
                db_params = {
                    'dbname': 'postgres',
                    'user': 'admin',
                    'password': 'admin',
                    'host': 'postgres-db',
                    'port': 5677
                }
                self.connection = psycopg2.connect(**db_params)
                self.cursor = self.connection.cursor()
                self.is_db_connected = True
                return True
            except Exception as err:
                logging.info(f"Database connection failed: {err}")
                pass
            time.sleep(1)
        return self.is_db_connected

    def validate_connection(self):
        if self.is_db_connected:
            return self.open_connection()
        return self.is_db_connected

    def __del__(self):
        if self.is_db_connected and self.cursor is not None:
            self.cursor.close()
            self.connection.close()