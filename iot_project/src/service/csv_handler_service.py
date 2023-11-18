import pandas as pd
import random
import os
from src.model.payload import Payload


class CsvHandlerService:
    FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'util', 'online.csv')

    def __init__(self):
        self.df = pd.read_csv(self.FILE_PATH, sep=';')

    def generate_payload_instance(self):
        row = self._get_random_row()
        payload = Payload(
            acceleration_x=row['acceleration_x'],
            acceleration_y=row['acceleration_y'],
            acceleration_z=row['acceleration_z'],
            gyro_x=row['gyro_x'],
            gyro_y=row['gyro_y'],
            gyro_z=row['gyro_z']
        )
        return payload.format()

    def _get_random_row(self):
        csv_size = len(self.df)
        line = random.randint(1, csv_size)
        return self.df.iloc[line - 1]
