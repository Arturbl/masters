import psycopg2
from datetime import datetime


class DatabaseHandlerService:

    def __init__(self):
        self.connection = self.open_connection()
        self.cursor = self.connection.cursor()

    def save(self, payload, activity):
        insert_query = '''
            INSERT INTO movement 
                (date, time, activity, acceleration_x, acceleration_y, acceleration_z, gyro_x, gyro_y, gyro_z)
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = self.build_movement_params(payload, activity)
        self.cursor.execute(insert_query, values)
        self.connection.commit()

    def validate_user_password(self, username, password):
        select_query = '''
                SELECT id FROM users
                WHERE username = %s AND password = %s
        '''
        values = (username, password)
        self.cursor.execute(select_query, values)
        result = self.cursor.fetchone()
        return result is not None

    def open_connection(self):
        db_params = {
            'dbname': 'postgres',
            'user': 'admin',
            'password': 'admin',
            'host': 'localhost',
            'port': 5677
        }
        return psycopg2.connect(**db_params)

    def __del__(self):
        self.cursor.close()
        self.connection.close()