CREATE TABLE movement (
    id SERIAL PRIMARY KEY,
    activity INT,
    acceleration_x FLOAT,
    acceleration_y FLOAT,
    acceleration_z FLOAT,
    gyro_x FLOAT,
    gyro_y FLOAT,
    gyro_z FLOAT,
    datetime DATETIME DEFAULT NULL
);


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    gender VARCHAR(1),
    age INT,
    height INT,
    weight INT
);

INSERT INTO users
    (username, password)
VALUES
    ('artur', 'artur');
