CREATE TABLE favorite_product (
    id SERIAL PRIMARY KEY,
    shopper_id INTEGER NOT NULL REFERENCES shopper,
    product_id INTEGER NOT NULL REFERENCES product,
    create_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
