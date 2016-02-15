CREATE TABLE shopping_mall (
    id SERIAL PRIMARY KEY,
    platform_id INT NOT NULL,
    product_sku VARCHAR(20) NOT NULL,
    name VARCHAR(64) NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    blurb VARCHAR(128),
    detail_images JSONB NOT NULL DEFAULT '{}'
)