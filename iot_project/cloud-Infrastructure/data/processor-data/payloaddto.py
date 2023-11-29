import json


class PayloadDto:

    def __init__(self):
        self.acceleration_x = None
        self.acceleration_y = None
        self.acceleration_z = None
        self.gyro_x = None
        self.gyro_y = None
        self.gyro_z = None

    def format(self):
        return (
            f'"acceleration_x":{self.acceleration_x},'
            f'"acceleration_y":{self.acceleration_y},'
            f'"acceleration_z":{self.acceleration_z},'
            f'"gyro_x":{self.gyro_x},'
            f'"gyro_y":{self.gyro_y},'
            f'"gyro_z":{self.gyro_z}}}'
        )

    def parse(self, body):
        data_dict = json.loads(body)
        self.acceleration_x = data_dict.get("acceleration_x", 0)
        self.acceleration_y = data_dict.get("acceleration_y", 0)
        self.acceleration_z = data_dict.get("acceleration_z", 0)
        self.gyro_x = data_dict.get("gyro_x", 0)
        self.gyro_y = data_dict.get("gyro_y", 0)
        self.gyro_z = data_dict.get("gyro_z", 0)

    def __str__(self) -> str:
        return (
            f'PayloadDto('
            f'acceleration_x={self.acceleration_x}, '
            f'acceleration_y={self.acceleration_y}, '
            f'acceleration_z={self.acceleration_z}, '
            f'gyro_x={self.gyro_x}, '
            f'gyro_y={self.gyro_y}, '
            f'gyro_z={self.gyro_z}'
            f')'
        )

