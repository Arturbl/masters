import pandas as pd
import random
import os
from src.model.payloaddto import PayloadDto


class CsvHandlerService:
    FILE_PATH = os.path.join(os.path.dirname(__file__), '../..', 'util', 'online.csv')

    def __init__(self):
        self.df = pd.read_csv(self.FILE_PATH, sep=';')
        self.index = 0

    def generate_payload_instance(self):
        row = self._get_random_row()
        payload_dto = PayloadDto()
        payload_dto.acceleration_x = row['acceleration_x']
        payload_dto.acceleration_y = row['acceleration_y']
        payload_dto.acceleration_z = row['acceleration_z']
        payload_dto.gyro_x = row['gyro_x']
        payload_dto.gyro_y = row['gyro_y']
        payload_dto.gyro_z = row['gyro_z']
        return payload_dto

    def _get_random_row(self):
        print(f'index: {self.index}')
        csv_size = len(self.df)
        if self.index <= csv_size:
            self.index += 1
        else:
            self.index = 0
        return self.df.iloc[self.index - 1]
