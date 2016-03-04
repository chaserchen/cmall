CREATE TABLE product (
    id INTERVAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    type INT NOT NULL,
    title VARCHAR(128),
    brand VARCHAR(64),
    detail_image VARCHAR(128)
);

CREATE TABLE platform (
    id INTERVAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    price VARCHAR(32) NOT NULL,
    product_url VARCHAR(128) NOT NULL
);
