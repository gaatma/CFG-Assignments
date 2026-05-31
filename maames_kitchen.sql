-- ---------------------------------------------------------
-- ASSIGNMENT 3: DATA AND MySQL
-- Theme: Maame's Kitchen – A Ghanaian Street Food Business
-- Scenario: My mother sells traditional Ghanaian food, Banku, Palm nut soup,  
--           Fish, Stew and Drinks on the streets of Agona Swedru, Ghana.
--           This database helps her track her menu, customers, orders, and what was ordered.
-- Author: GIFTY ACQUAH
-- Date:   18TH APRIL 2026
-- ---------------------------------------------------------


-- ---------------------------------------------------------
--  CREATE AND SELECT THE DATABASE
-- ---------------------------------------------------------

-- Create the database (only if it doesn't already exist)
CREATE DATABASE IF NOT EXISTS maames_kitchen;

-- Tell MySQL to use this database for all commands below
USE maames_kitchen;


-- ---------------------------------------------------------
--  CREATE TABLES
--  create 4 tables:
--   1. menu_items   – the food Maame sells
--   2. customers    – her regular customers
--   3. orders       – each sale/transaction
--   4. order_items  – the individual food items inside each order
-- ---------------------------------------------------------


-- ------------------------------------------------------------
-- TABLE 1: menu_items
-- Stores each food or drink Maame sells
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS menu_items (
    item_id       INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each menu item, auto-increases
    name          VARCHAR(100) NOT NULL,            -- Name of the dish, e.g. 'Banku with Tilapia'
    category      VARCHAR(50) NOT NULL,             -- Type of food: 'Main', 'Soup', 'Stew', 'Drink'
    price         DECIMAL(10, 2) NOT NULL,          -- Price in Ghana Cedis, e.g. 25.00
    calories      INT,                              -- Approximate calories (optional)
    is_available  BOOLEAN NOT NULL DEFAULT TRUE     -- Is this dish available today? TRUE = yes
    -- Constraints used: NOT NULL (on name, category, price, is_available), DEFAULT (on is_available)
);


-- ------------------------------------------------------------
-- TABLE 2: customers
-- Stores Maame's regular customers
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (
    customer_id   INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each customer
    first_name    VARCHAR(50) NOT NULL,             -- Customer's first name
    last_name     VARCHAR(50) NOT NULL,             -- Customer's last name
    phone_number  VARCHAR(20) UNIQUE,               -- Phone number (must be unique per customer)
    joined_date   DATE NOT NULL                     -- The date they became a regular customer
    -- Constraints used: NOT NULL, UNIQUE (on phone_number)
);


-- ------------------------------------------------------------
-- TABLE 3: orders
-- Stores each transaction/sale Maame makes
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (
    order_id        INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each order
    customer_id     INT NOT NULL,                    -- Links to which customer placed the order
    order_date      DATETIME NOT NULL DEFAULT NOW(), -- Date and time of the order
    total_amount    DECIMAL(10, 2) NOT NULL,         -- Total cost of the order in Ghana Cedis
    payment_method  VARCHAR(20) NOT NULL DEFAULT 'Cash', -- How they paid: 'Cash' or 'MoMo'

    -- FOREIGN KEY: connects customer_id here to customer_id in the customers table
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);


-- ------------------------------------------------------------
-- TABLE 4: order_items
-- Stores the individual food items that belong to each order
-- This table links orders to menu_items
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id  INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each line item
    order_id       INT NOT NULL,                    -- Links to which order this belongs to
    item_id        INT NOT NULL,                    -- Links to which menu item was ordered
    quantity       INT NOT NULL DEFAULT 1,          -- How many of this item were ordered
    unit_price     DECIMAL(10, 2) NOT NULL,         -- Price at time of order (in case price changes later)

    -- FOREIGN KEY: links to the orders table
    FOREIGN KEY (order_id) REFERENCES orders(order_id),

    -- FOREIGN KEY: links to the menu_items table
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id),

    -- CONSTRAINT: quantity must be at least 1 (you can't order 0 items!)
    CONSTRAINT chk_quantity CHECK (quantity >= 1)
);


-- ---------------------------------------------------------
-- STEP 3: INSERT MOCK DATA
-- insert at least 8 rows into each table
-- ---------------------------------------------------------


-- ------------------------------------------------------------
-- INSERT INTO menu_items 
-- Maame's full menu of Ghanaian dishes
-- ------------------------------------------------------------
INSERT INTO menu_items (name, category, price, calories, is_available) VALUES
    ('Banku with Tilapia',         'Main',  25.00, 650, TRUE),
    ('Banku with Okro Stew',       'Main',  20.00, 580, TRUE),
    ('Palm Nut Soup with Fufu',    'Main',  30.00, 720, TRUE),
    ('Tomato Stew with Fried Fish','Stew',  18.00, 500, TRUE),
    ('Plain Banku',                'Main',  10.00, 350, TRUE),
    ('Kelewele',                   'Snack',  8.00, 280, TRUE),
    ('Sobolo Drink',               'Drink',  5.00, 120, TRUE),
    ('Groundnut Soup with Rice',   'Main',  28.00, 700, FALSE);

-- 'Groundnut Soup with Rice' is marked FALSE (not available today)


-- ------------------------------------------------------------
-- INSERT INTO customers 
-- Maame's regular customers in the neighbourhood
-- ------------------------------------------------------------
INSERT INTO customers (first_name, last_name, phone_number, joined_date) VALUES
    ('Akosua',   'Mensah',   '0244000001', '2023-01-15'),
    ('Kwame',    'Asante',   '0244000002', '2023-03-20'),
    ('Abena',    'Boateng',  '0244000003', '2023-05-10'),
    ('Kofi',     'Otieno',   '0244000004', '2023-07-01'),
    ('Ama',      'Darko',    '0244000005', '2023-08-22'),
    ('Yaw',      'Adjei',    '0244000006', '2023-09-14'),
    ('Efua',     'Quaye',    '0244000007', '2024-01-05'),
    ('Nana',     'Owusu',    '0244000008', '2024-02-18');


-- ------------------------------------------------------------
-- INSERT INTO orders 
-- Each row is one transaction by a customer
-- Palm Nut 30.00 + Banku 25.00 + Sobolo 5.00 = 60.00
-- Banku 25.00 + Sobolo x2 10.00 = 35.00
-- ------------------------------------------------------------
INSERT INTO orders (customer_id, order_date, total_amount, payment_method) VALUES
    (1, '2024-03-01 12:00:00', 35.00, 'Cash'),  
    (2, '2024-03-01 12:30:00', 30.00, 'MoMo'),
    (3, '2024-03-02 13:00:00', 18.00, 'Cash'),
    (4, '2024-03-02 13:15:00', 25.00, 'Cash'),
    (5, '2024-03-03 11:45:00', 33.00, 'MoMo'),
    (6, '2024-03-03 12:00:00', 20.00, 'Cash'),
    (7, '2024-03-04 14:00:00', 60.00, 'MoMo'), 
    (8, '2024-03-04 14:30:00', 10.00, 'Cash');


-- ------------------------------------------------------------
-- INSERT INTO order_items (8+ rows)
-- Each row is one food item inside an order
-- ------------------------------------------------------------
INSERT INTO order_items (order_id, item_id, quantity, unit_price) VALUES
    (1, 1, 1, 25.00),   -- Order 1: Banku with Tilapia x1 = 25.00
    (1, 7, 2,  5.00),   -- Order 1: Sobolo Drink x2 = 10.00 | Order 1 subtotal = 35.00
    (2, 3, 1, 30.00),   -- Order 2: Palm Nut Soup with Fufu x1
    (3, 4, 1, 18.00),   -- Order 3: Tomato Stew with Fried Fish x1
    (4, 1, 1, 25.00),   -- Order 4: Banku with Tilapia x1
    (5, 2, 1, 20.00),   -- Order 5: Banku with Okro Stew x1
    (5, 6, 1,  8.00),   -- Order 5: Kelewele x1
    (5, 7, 1,  5.00),   -- Order 5: Sobolo Drink x1
    (6, 2, 1, 20.00),   -- Order 6: Banku with Okro Stew x1
    (7, 3, 1, 30.00),   -- Order 7: Palm Nut Soup with Fufu x1
    (7, 1, 1, 25.00),   -- Order 7: Banku with Tilapia x1
    (7, 7, 1,  5.00),   -- Order 7: Sobolo Drink x1 | Order 7 subtotal = 60.00
    (8, 5, 1, 10.00);   -- Order 8: Plain Banku x1


-- ---------------------------------------------------------
--  RETRIEVE DATA – At least 5 SELECT queries
-- ---------------------------------------------------------


-- ------------------------------------------------------------
--  Show the full menu, sorted by category then price
-- ------------------------------------------------------------
SELECT
    item_id,
    name,
    category,
    price,
    is_available
FROM menu_items
ORDER BY category, price ASC;


-- ------------------------------------------------------------
--  Show all customers, sorted alphabetically by last name
-- ------------------------------------------------------------
SELECT
    customer_id,
    first_name,
    last_name,
    phone_number,
    joined_date
FROM customers
ORDER BY last_name ASC;


-- ------------------------------------------------------------
-- Show all orders with customer names (JOIN)
-- join orders and customers to show the full picture
-- Built-in function: CONCAT
-- ------------------------------------------------------------
SELECT
    o.order_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,  
    o.order_date,
    o.total_amount,
    o.payment_method
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date DESC;


-- ------------------------------------------------------------
--  Show order details with food names (JOIN across 3 tables)
--  join order_items, menu_items, and orders together
-- ------------------------------------------------------------
SELECT
    oi.order_item_id,
    o.order_id,
    m.name              AS food_item,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS line_total   
FROM order_items oi
JOIN orders o      ON oi.order_id = o.order_id
JOIN menu_items m  ON oi.item_id  = m.item_id
ORDER BY o.order_id, m.name;


-- ------------------------------------------------------------
--  Show only available menu items priced under 25 cedis
-- ------------------------------------------------------------
SELECT
    name,
    category,
    price
FROM menu_items
WHERE is_available = TRUE AND price < 25.00
ORDER BY price ASC;


-- ------------------------------------------------------------
-- Show customers who joined in 2024
-- Uses built-in function YEAR() to extract the year from a date
-- ------------------------------------------------------------
SELECT
    first_name,
    last_name,
    phone_number,
    joined_date
FROM customers
WHERE YEAR(joined_date) = 2024     
ORDER BY joined_date ASC;


-- ------------------------------------------------------------
--  Show each order with a formatted date
-- Uses built-in function DATE_FORMAT()
-- ------------------------------------------------------------
SELECT
    order_id,
    DATE_FORMAT(order_date, '%W %d %M %Y') AS formatted_date,  
    total_amount,
    payment_method
FROM orders
ORDER BY order_date ASC;


-- ---------------------------------------------------------
--  AGGREGATE FUNCTIONS
-- ---------------------------------------------------------


-- ------------------------------------------------------------
-- A Total revenue Maame has earned
-- SUM: adds up all order totals
-- AVG: average spend per order
-- COUNT: how many orders total
-- ------------------------------------------------------------
SELECT
    SUM(total_amount)   AS total_revenue,   
    AVG(total_amount)   AS average_order,  
    COUNT(order_id)     AS total_orders     
FROM orders;


-- ------------------------------------------------------------
--  Revenue broken down by payment method
-- ------------------------------------------------------------
SELECT
    payment_method,
    COUNT(order_id)    AS number_of_orders,
    SUM(total_amount)  AS total_revenue
FROM orders
GROUP BY payment_method
ORDER BY total_revenue DESC;


-- ------------------------------------------------------------
-- Most popular menu items (by quantity sold)
-- Used SUM aggregate to count total sold
-- ------------------------------------------------------------
SELECT
    m.name             AS food_item,
    SUM(oi.quantity)   AS total_sold       
FROM order_items oi
JOIN menu_items m ON oi.item_id = m.item_id
GROUP BY m.name
ORDER BY total_sold DESC;


-- ---------------------------------------------------------
-- DELETE DATA
-- Scenario: Customer 8 (Nana) cancelled her Plain Banku order
-- ---------------------------------------------------------

-- query to see the order before deleting
SELECT * FROM order_items WHERE order_id = 8;

-- query to delete it
DELETE FROM order_items
WHERE order_id = 8 AND item_id = 5;

-- query to remove the empty order record
DELETE FROM orders
WHERE order_id = 8;

-- query to confirm it's gone
SELECT * FROM order_items WHERE order_id = 8;


-- ---------------------------------------------------------
--        STORED PROCEDURE
-- Scenario: Maame wants to quickly look up all orders
--           placed by a specific customer by their ID
-- ---------------------------------------------------------

-- Drop procedure if it already exists 
DROP PROCEDURE IF EXISTS GetCustomerOrders;

-- Use the $$ delimiter 
DELIMITER $$

CREATE PROCEDURE GetCustomerOrders(IN cust_id INT)
BEGIN
    -- check the customer ID provided is valid
    IF cust_id IS NULL THEN
        SELECT 'Error: Please provide a valid customer ID.' AS message;
    ELSEIF NOT EXISTS (SELECT 1 FROM customers WHERE customer_id = cust_id) THEN
        SELECT CONCAT('Error: No customer found with ID ', cust_id) AS message;
    ELSE
        -- This procedure takes a customer ID as input
        -- and returns all their orders with food details
        SELECT
            o.order_id,
            CONCAT(c.first_name, ' ', c.last_name)        AS customer_name,
            DATE_FORMAT(o.order_date, '%d %M %Y')          AS order_date,
            m.name                                         AS food_item,
            oi.quantity,
            oi.unit_price,
            o.payment_method
        FROM orders o
        JOIN customers c    ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id    = oi.order_id
        JOIN menu_items m   ON oi.item_id    = m.item_id
        WHERE o.customer_id = cust_id
        ORDER BY o.order_date DESC;
    END IF;

END $$

-- The delimiter back to normal
DELIMITER ;

-- ---------------------------------------------------------
-- DEMO: Call the stored procedure
-- Example: Show all orders placed by customer 1 (Akosua Mensah)
-- ---------------------------------------------------------
CALL GetCustomerOrders(1);

-- Example: Show all orders placed by customer 5 (Ama Darko)
CALL GetCustomerOrders(5);


-- ---------------------------------------------------------
-- REAL-LIFE SCENARIO WALKTHROUGH
-- Imagine it's lunchtime on the streets of Agona Swedru in Ghana.
-- A new customer, Kweku, walks up to Maame's food stand.
-- ---------------------------------------------------------

-- 1. Kweku is a new customer — add him to the system
INSERT INTO customers (first_name, last_name, phone_number, joined_date)
VALUES ('Kweku', 'Amponsah', '0244000099', CURDATE());  

-- 2. Kweku orders Palm Nut Soup with Fufu and a Sobolo Drink
INSERT INTO orders (customer_id, order_date, total_amount, payment_method)
VALUES (
    (SELECT customer_id FROM customers WHERE phone_number = '0244000099'),
    NOW(),   
    35.00,
    'MoMo'
);

-- 3. Add the items to his order
INSERT INTO order_items (order_id, item_id, quantity, unit_price)
VALUES
    (LAST_INSERT_ID(), 3, 1, 30.00),   -- Palm Nut Soup with Fufu
    (LAST_INSERT_ID(), 7, 1,  5.00);   -- Sobolo Drink

-- 4. Oh! Kweku actually didn't want the Sobolo. Remove it.
DELETE FROM order_items
WHERE order_id = (SELECT order_id FROM orders WHERE customer_id =
    (SELECT customer_id FROM customers WHERE phone_number = '0244000099'))
AND item_id = 7;

-- 5. Check Kweku's final order using our stored procedure
CALL GetCustomerOrders(
    (SELECT customer_id FROM customers WHERE phone_number = '0244000099')
);

-- ---------------------------------------------------------
-- BONUS: UPDATE QUERY
-- Scenario: Maame increases prices of all Main dishes by 2 cedis
--           due to rising ingredient costs
-- ---------------------------------------------------------

-- Check prices before the update
SELECT name, category, price FROM menu_items WHERE category = 'Main' ORDER BY name;

-- Apply the price increase
UPDATE menu_items
SET price = price + 2.00
WHERE category = 'Main';

-- Confirm the new prices
SELECT name, category, price FROM menu_items WHERE category = 'Main' ORDER BY name;


-- ---------------------------------------------------------
-- End Of Maame's Kitchen Data Management
