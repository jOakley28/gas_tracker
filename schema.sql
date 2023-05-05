/*
    Table to store cars and their information 
*/
CREATE TABLE cars (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner TEXT,
    make TEXT,
    model TEXT,
    year INTEGER,
    mpg INTEGER,
    tank_size INTEGER
);


/*
    Create a table to store gas purchase information
*/
CREATE TABLE gas (
    gas_id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    date DATE,
    cost NUMERIC, 
    amount NUMERIC,
    distance NUMERIC,
    cost_per_gallon NUMERIC,
    trip_mpg NUMERIC,
    distance_remaining NUMERIC,
    phase string, 
    foreign key (car_id) references cars(car_id)
);
