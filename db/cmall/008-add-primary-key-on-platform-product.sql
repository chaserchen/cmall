ALTER TABLE platform_product DROP CONSTRAINT platform_pkey;
ALTER TABLE platform_product RENAME COLUMN name TO platform_name;
ALTER TABLE platform_product ADD PRIMARY KEY (platform_name, product_id, created_at);
