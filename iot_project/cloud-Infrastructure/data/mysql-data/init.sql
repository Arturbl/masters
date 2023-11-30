CREATE TABLE movement (
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

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    age INT,
    height INT,
    weight INT
);

INSERT INTO users
    (username, password)
VALUES
    ('artur', 'artur');
