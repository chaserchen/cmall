DROP TABLE shopper;
CREATE TABLE shopper (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    mobile VARCHAR(16) NOT NULL,
    email VARCHAR(32)
);
