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

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    age INT,
    height INT,
    weight INT
);

INSERT INTO Users
    (username, password)
VALUES
    ('artur', 'artur');
