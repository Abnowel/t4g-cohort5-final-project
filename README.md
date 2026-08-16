# Jewelry Inventory & Order Management System

A full-stack jewelry inventory and order management system built with FastAPI, SQLAlchemy, MySQL, HTML, CSS, and JavaScript.

The system provides a REST API and a web dashboard for managing customers, jewelry inventory, and orders. It also handles stock validation and automatically updates inventory when orders are created, cancelled, or deleted.

This project was developed as part of the Tech4Girls final project. The system can also be adapted and customized for use by individual jewelry businesses.


## 1. Features

### 1.1 Customer Management

1. Create customers
2. View all customers
3. View individual customers
4. Update customer information
5. Delete customers
6. Prevent duplicate email addresses
7. Prevent duplicate phone numbers
8. Prevent deletion of customers with existing orders

### 1.2 Jewelry Management

1. Create jewelry items
2. View all jewelry items
3. View individual jewelry items
4. Update jewelry information
5. Delete jewelry items
6. Prevent duplicate jewelry names
7. Track stock quantity
8. Validate prices and stock values
9. Prevent deletion of jewelry items connected to existing orders

### 1.3 Order Management

1. Create orders
2. View all orders
3. View individual orders
4. Update order status
5. Delete orders
6. Calculate order totals automatically
7. Check that the customer exists
8. Check that jewelry items exist
9. Check available stock
10. Validate order status changes

### 1.4 Inventory Management

1. Reduce jewelry stock when an order is created
2. Restore stock when an order is cancelled
3. Restore stock when an order is deleted
4. Prevent orders when there is not enough stock

### 1.5 Dashboard

The dashboard displays:

1. Total customers
2. Total jewelry items
3. Total orders
4. Total sales
5. Customer records
6. Jewelry inventory
7. Order records

The dashboard also allows users to create and manage customers, jewelry items, and orders.


## 2. Technologies Used

### 2.1 Backend

1. Python
2. FastAPI
3. SQLAlchemy
4. MySQL
5. Pydantic
6. Uvicorn
7. python-dotenv

### 2.2 Frontend

1. HTML5
2. CSS3
3. JavaScript

### 2.3 API Testing

1. Postman
2. FastAPI Swagger documentation

### 2.4 Development Tools

1. Visual Studio Code
2. Git
3. GitHub


## 3. Project Structure

t4g-cohort5-final-project/
|
├── frontend/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── main.js
│   │
│   └── index.html
│
├── models/
│   ├── base_model.py
│   ├── customers_model.py
│   ├── jewelry_model.py
│   ├── order_model.py
│   └── order_item_model.py
│
├── routes/
│   ├── customer_route.py
│   ├── jewelry_route.py
│   ├── order_route.py
│   └── order_item_route.py
│
├── services/
│   ├── customer_service.py
│   ├── jewelry_service.py
│   ├── order_service.py
│   └── order_item_service.py
│
├── utils/
│   ├── database_connection.py
│   └── uuid_generate.py
│
├── main.py
├── requirements.txt
└── README.md

## 4. Database Relationships

The project uses relationships between customers, orders, order items, and jewelry.

Customer
   |
   | one
   |
   | many
   v
 Order
   |
   | one
   |
   | many
   v
OrderItem
   |
   | many
   |
   | one
   v
Jewelry


A customer can have multiple orders.

An order can contain one or more order items.

A jewelry item can appear in multiple order items.

The OrderItem table connects orders and jewelry items while storing the quantity and price for each item in an order.

## 5. API Endpoints

### 5.1 Customers

| Method | Endpoint          | Description       |
| ------ | ----------------- | ----------------- |
| GET    | `/customers/`     | Get all customers |
| GET    | `/customers/{id}` | Get a customer    |
| POST   | `/customers/`     | Create a customer |
| PUT    | `/customers/{id}` | Update a customer |
| DELETE | `/customers/{id}` | Delete a customer |

### 5.2 Jewelry

| Method | Endpoint        | Description           |
| ------ | --------------- | --------------------- |
| GET    | `/jewelry/`     | Get all jewelry items |
| GET    | `/jewelry/{id}` | Get a jewelry item    |
| POST   | `/jewelry/`     | Create a jewelry item |
| PUT    | `/jewelry/{id}` | Update a jewelry item |
| DELETE | `/jewelry/{id}` | Delete a jewelry item |

### 5.3 Orders

| Method | Endpoint       | Description     |
| ------ | -------------- | --------------- |
| GET    | `/orders/`     | Get all orders  |
| GET    | `/orders/{id}` | Get an order    |
| POST   | `/orders/`     | Create an order |
| PUT    | `/orders/{id}` | Update an order |
| DELETE | `/orders/{id}` | Delete an order |

## 6. Order Creation

When an order is created, the system:

1. Checks that the customer exists.
2. Checks that the jewelry items exist.
3. Checks that enough stock is available.
4. Creates the order.
5. Creates the related order items.
6. Calculates the order total.
7. Reduces the jewelry stock.
8. Saves the changes to the database.

Example request:

{
    "customer_id": "customer-id",
    "items": [
        {
            "jewelry_id": "jewelry-id",
            "quantity": 2
        }
    ]
}


## 7. Inventory Management

The system automatically manages stock when orders are processed.

For example, if a jewelry item has 10 units in stock and a customer orders 2:

Stock before order: 10
Quantity ordered: 2
Stock after order: 8


If the order is cancelled, the stock is restored:

Stock before cancellation: 8
Cancelled quantity: 2
Stock after cancellation: 10


The same stock restoration is applied when an order is deleted.

## 8. Validation and Error Handling

The system includes validation and error handling to protect the data.

The main validation rules include:

1. Customers must exist before an order can be created.
2. Jewelry items must exist before they can be added to an order.
3. An order cannot be created when there is insufficient stock.
4. Jewelry prices must be valid.
5. Stock quantities cannot be negative.
6. Duplicate customer emails are not allowed.
7. Duplicate customer phone numbers are not allowed.
8. Duplicate jewelry names are not allowed.
9. Customers with existing orders cannot be deleted.
10. Jewelry items connected to existing orders cannot be deleted.
11. Invalid order status changes are rejected.

The API also returns appropriate HTTP status codes for successful requests and errors.

## 9. Running the Project

### 9.1 Clone the Repository


git clone <your-github-repository-url>
cd t4g-cohort5-final-project


### 9.2 Create a Virtual Environment

python -m venv venv


### 9.3 Activate the Virtual Environment

On Windows:
venv\Scripts\activate


On Linux or macOS:
source venv/bin/activate

### 9.4 Install the Required Packages

pip install -r requirements.txt

### 9.5 Configure the Database

Create a `.env` file in the project root and add your MySQL database connection details.

Example:

DATABASE_URL=mysql+mysqlconnector://username:password@localhost/database_name


Replace the username, password, and database name with your own values.

Do not upload your `.env` file to GitHub.

### 9.6 Start the Application
uvicorn main:app --reload


The application will be available at:

http://127.0.0.1:8000


## 10. API Documentation

FastAPI provides interactive API documentation.

After starting the application, open:

http://127.0.0.1:8000/docs

Swagger can be used to view and test the available API endpoints.

## 11. Frontend

The project includes a web dashboard connected to the FastAPI backend.

The dashboard allows users to:

1. View customer information
2. Manage customers
3. View jewelry inventory
4. Manage jewelry items
5. Create orders
6. Update order status
7. Delete orders
8. Monitor stock levels
9. View basic sales information

The frontend communicates with the backend using JavaScript fetch requests.

## 12. Testing

The API was tested using Postman and the FastAPI Swagger documentation.

The following areas were tested:

1. Customer CRUD operations
2. Jewelry CRUD operations
3. Order CRUD operations
4. Duplicate customer validation
5. Duplicate jewelry validation
6. Insufficient stock validation
7. Stock reduction after order creation
8. Stock restoration after order cancellation
9. Stock restoration after order deletion
10. Customer deletion restrictions
11. Jewelry deletion restrictions
12. Order status validation

The frontend was also tested for customer, jewelry, and order management.

## 13. Future Improvements

Possible improvements for future versions include:

1. User login and authentication
2. Staff accounts and permissions
3. Search and filtering
4. Sales reports
5. Printable invoices and receipts
6. Customer purchase history
7. Low stock notifications
8. Product images
9. Barcode or QR code support
10. Payment tracking
11. More detailed business reports
12. Cloud deployment
13. Automated tests
14. Mobile-friendly improvements

## 14. Project Background

This project was developed as the final project for the Tech4Girls program.

It allowed me to apply the skills I learned in:

1. Python
2. FastAPI
3. REST API development
4. SQLAlchemy
5. MySQL
6. CRUD operations
7. Database relationships
8. Data validation
9. Business logic
10. Frontend development
11. Git and GitHub

The system was built around a jewelry business use case and can be further customized based on the needs of a particular jewelry store.

## 15. Author

**Abnowel Ewurabena Sam**

Backend Developer

Tech4Girls Cohort 5

## 16. License

This project is currently intended as a portfolio and educational project.
