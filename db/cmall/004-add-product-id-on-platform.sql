ALTER TABLE platform ADD COLUMN product_id INT NOT NULL;
ALTER TABLE platform DROP COLUMN id;

ALTER TABLE platform ADD PRIMARY KEY (product_id, created_at);
