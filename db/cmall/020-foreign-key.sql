ALTER TABLE platform_product ADD FOREIGN KEY (product_id) REFERENCES product(id);
ALTER TABLE product ADD FOREIGN KEY (product_url) REFERENCES product_url(url);
ALTER TABLE promotion ADD FOREIGN KEY (product_id) REFERENCES product(id);