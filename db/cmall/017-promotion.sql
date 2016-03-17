CREATE TABLE promotion (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    end_at TIMESTAMP WITH TIME ZONE NOT NULL,
    type INT NOT NULL,
    detail_image VARCHAR(64)
);
