-- Criando o esquema do banco
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price NUMERIC(10, 2)
);

CREATE TABLE customers (
    id SERIAL  PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales (
    id SERIAL  PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    customer_id INTEGER REFERENCES customers(id),
    quantity INTEGER NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    sale_date TIMESTAMP NOT NULL
);

-- Inserindo dados na tabela products
INSERT INTO products (sku, name, category, price) VALUES ('SKU001', 'Product A', 'Category 1', 10.99);
INSERT INTO products (sku, name, category, price) VALUES ('SKU002', 'Product B', 'Category 1', 20.50);
INSERT INTO products (sku, name, category, price) VALUES ('SKU003', 'Product C', 'Category 2', 15.75);
INSERT INTO products (sku, name, category, price) VALUES ('SKU004', 'Product D', 'Category 3', 30.00);
INSERT INTO products (sku, name, category, price) VALUES ('SKU005', 'Product E', 'Category 4', 25.00);

-- Inserindo dados na tabela customers
INSERT INTO customers (name, email) VALUES ('John Doe', 'john@example.com');
INSERT INTO customers (name, email) VALUES ('Jane Smith', 'jane@example.com');
INSERT INTO customers (name, email) VALUES ('Bob Johnson', 'bob@example.com');
INSERT INTO customers (name, email) VALUES ('Alice Brown', 'alice@example.com');
INSERT INTO customers (name, email) VALUES ('Charlie Davis', 'charlie@example.com');

-- Inserindo dados na tabela sales
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 1, 4, 120.00, '2025-01-17 12:22:49');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 1, 7, 175.00, '2025-01-28 04:04:17');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 4, 4, 100.00, '2025-02-04 11:58:16');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 2, 2, 21.98, '2025-01-05 10:30:45');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 3, 1, 20.50, '2025-01-06 15:15:10');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 5, 3, 47.25, '2025-01-08 09:45:22');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 2, 1, 30.00, '2025-01-10 17:22:30');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 4, 5, 125.00, '2025-01-12 11:00:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 3, 2, 21.98, '2025-01-14 18:25:45');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 5, 6, 123.00, '2025-01-15 13:12:22');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 1, 2, 31.50, '2025-01-18 08:10:33');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 4, 1, 30.00, '2025-01-20 14:05:20');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 2, 3, 75.00, '2025-01-23 19:30:40');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 5, 2, 21.98, '2025-01-25 10:45:10');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 4, 4, 82.00, '2025-01-29 16:20:50');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 2, 1, 15.75, '2025-02-01 12:00:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 5, 2, 60.00, '2025-02-03 18:40:30');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 1, 8, 200.00, '2025-02-05 11:25:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 4, 3, 32.97, '2025-02-07 14:50:10');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 3, 2, 41.00, '2025-02-08 10:20:15');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 5, 4, 63.00, '2025-02-10 16:45:55');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 2, 1, 30.00, '2025-02-12 20:30:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 3, 2, 50.00, '2025-02-15 09:10:10');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 1, 6, 65.94, '2025-02-16 13:35:30');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 4, 2, 41.00, '2025-02-18 15:00:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 2, 3, 47.25, '2025-02-19 11:30:45');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 5, 2, 60.00, '2025-02-21 14:10:22');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 4, 1, 25.00, '2025-02-22 19:45:55');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 2, 7, 76.93, '2025-02-24 12:10:10');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 1, 4, 82.00, '2025-02-25 17:30:50');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 3, 5, 78.75, '2025-02-27 09:55:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 5, 3, 90.00, '2025-02-28 14:25:30');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 2, 9, 225.00, '2025-03-02 10:00:00');
