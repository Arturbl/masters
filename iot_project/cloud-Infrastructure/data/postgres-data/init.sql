CREATE TABLE Movement (
    id SERIAL PRIMARY KEY,
    date DATE,
    time TIME,
    activity INT,
    acceleration_x FLOAT,
    acceleration_y FLOAT,
    acceleration_z FLOAT,
    gyro_x FLOAT,
    gyro_y FLOAT,
    gyro_z FLOAT
);
