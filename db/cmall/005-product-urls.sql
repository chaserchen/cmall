CREATE TABLE product_urls (
    id SERIAL PRIMARY KEY,
    platform_id INT NOT NULL,
    type INT NOT NULL,
    url VARCHAR(64) NOT NULL
)
