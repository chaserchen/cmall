CREATE TABLE operator (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    password VARCHAR(128) NOT NULL,
    mobile VARCHAR(16) NOT NULL,
    role INT NOT NULL
);
