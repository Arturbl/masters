

class Payload:

    MODEL = "training-DT"

    def __init__(self, acceleration_x, acceleration_y, acceleration_z, gyro_x, gyro_y, gyro_z):
        self.acceleration_x = acceleration_x
        self.acceleration_y = acceleration_y
        self.acceleration_z = acceleration_z
        self.gyro_x = gyro_x
        self.gyro_y = gyro_y
        self.gyro_z = gyro_z

    def format(self):
        return [
            f'{{"model":"{self.MODEL}",'
            f'"acceleration_x":{self.acceleration_x},'
            f'"acceleration_y":{self.acceleration_y},'
            f'"acceleration_z":{self.acceleration_z},'
            f'"gyro_x":{self.gyro_x},'
            f'"gyro_y":{self.gyro_y},'
            f'"gyro_z":{self.gyro_z}}}'
        ]