CREATE TABLE Movement (
    id int primary key not null,
    date date,
    time time,
    activity int,
    acceleration_x float,
    acceleration_y float,
    acceleration_z float,
    gyro_x float,
    gyro_y float,
    gyro_z float
);