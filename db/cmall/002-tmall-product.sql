CREATE TABLE tmall_product(
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    category INT NOT NULL,
    detail_image VARCHAR(256) NOT NULL,
    store_url VARCHAR(256),
    stores_url VARCHAR(256),
    blurb VARCHAR(128)
);