
create database restaurant;
use restaurant;
CREATE TABLE Restaurant (
    id INT  PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255)
);


CREATE TABLE Menu (
    id INT  PRIMARY KEY,
    restaurant_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id) 
);


CREATE TABLE MenuItem (
    id INT  PRIMARY KEY,
    menu_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES Menu(id)
);


CREATE TABLE Customer (
    id INT  PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    address VARCHAR(255)
);


CREATE TABLE `Order` (
    id INT  PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(id) 
);


CREATE TABLE OrderItem (
    id INT  PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `Order`(id) ,
    FOREIGN KEY (menu_item_id) REFERENCES MenuItem(id) 
);


CREATE TABLE Payment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATETIME NOT NULL ,
    payment_method VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `Order`(id) 
);


CREATE TABLE Delivery (
    id INT  PRIMARY KEY,
    order_id INT NOT NULL,
    delivery_date DATETIME,
    status VARCHAR(50) NOT NULL,
    delivery_person VARCHAR(255),
    FOREIGN KEY (order_id) REFERENCES `Order`(id) 
);

