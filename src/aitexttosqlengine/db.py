from __future__ import annotations

import time
import psycopg
from typing import Iterable


class DatabaseManager:
    def __init__(self, dsn: str):
        start = time.perf_counter()
        self.conn = psycopg.connect(dsn, autocommit=True)
        elapsed = time.perf_counter() - start
        print(f"DB connect time: {elapsed:.3f}s")

    def initialize_schema(self) -> None:
        self.conn.execute("""
            DROP TABLE IF EXISTS orders;
            DROP TABLE IF EXISTS products;
            DROP TABLE IF EXISTS customers;
        """)
        self.conn.execute("""
            CREATE TABLE customers (
                customer_id INT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                country VARCHAR(100) NOT NULL
            );

            CREATE TABLE products (
                product_id INT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(100) NOT NULL,
                price DECIMAL(10,2) NOT NULL
            );

            CREATE TABLE orders (
                order_id INT PRIMARY KEY,
                customer_id INT NOT NULL,
                order_date DATE NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            );
        """)

    def seed_data(self) -> None:
        self.conn.execute("""
            INSERT INTO customers (customer_id, name, email, country) VALUES
                (1, 'Alice Johnson', 'alice@example.com', 'USA'),
                (2, 'Bob Smith', 'bob@example.com', 'Canada'),
                (3, 'Charlie Brown', 'charlie@example.com', 'UK'),
                (4, 'Diana Prince', 'diana@example.com', 'India'),
                (5, 'Ethan Hunt', 'ethan@example.com', 'Australia');

            INSERT INTO products (product_id, name, category, price) VALUES
                (101, 'Laptop', 'Electronics', 1200.00),
                (102, 'Smartphone', 'Electronics', 800.00),
                (103, 'Headphones', 'Accessories', 150.00),
                (104, 'Office Chair', 'Furniture', 250.00),
                (105, 'Coffee Maker', 'Home Appliances', 90.00);

            INSERT INTO orders (order_id, customer_id, order_date, amount) VALUES
                (1001, 1, '2025-01-10', 1200.00),
                (1002, 2, '2025-01-12', 800.00),
                (1003, 1, '2025-02-05', 150.00),
                (1004, 3, '2025-02-15', 250.00),
                (1005, 4, '2025-03-01', 1200.00),
                (1006, 5, '2025-03-10', 90.00),
                (1007, 2, '2025-03-15', 150.00),
                (1008, 4, '2025-04-01', 800.00),
                (1009, 1, '2025-04-12', 250.00),
                (1010, 3, '2025-05-05', 90.00);
        """)

    def execute(self, query: str):
        return self.conn.execute(query)

    def query(self, query: str):
        start = time.perf_counter()
        result = self.conn.execute(query)
        elapsed = time.perf_counter() - start
        print(f"DB query time: {elapsed:.3f}s")
        headers = [column.name for column in result.description] if result.description else []
        return headers, result.fetchall()

    def close(self) -> None:
        self.conn.close()
