CREATE TABLE store(
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES tmall_product(id),
    store_name VARCHAR(128) NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    product_url VARCHAR(256) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);