DROP TABLE product;

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    type INT NOT NULL,
    title VARCHAR(128),
    brand VARCHAR(64),
    detail_image VARCHAR(128),
    product_url VARCHAR(128) NOT NULL
);
