# 🍕 Joey's Pizza Delivery App

## Project Overview

Joey's Pizza Delivery is a feature-rich pizza ordering system built with FastAPI and MongoDB. Users can browse a dynamic menu, customize orders, manage their cart, and perform CRUD operations on their orders. The app includes secure user authentication and an admin dashboard for order management.

## Features

### 🔒 User Authentication
- Secure sessions for user authentication.
- Access control for order-related actions.

### 📋 Pizza Menu
- Display a list of pizzas from the database.
- Each pizza includes an image, flavor, and "Add to Cart" button.

### 📦 Order Management
- Create, update, and delete orders.
- View all orders placed by the user.

### 🛒 Cart Functionality
- Add pizzas to the cart with selected crust and size.
- View and manage cart contents.
- Update or remove items from the cart.

### 📡 API Endpoints

#### Auth Routes
- `GET /auth/signup` - Display signup page.
- `POST /auth/signup` - Handle user signup.
- `GET /auth/login` - Display login page.
- `POST /auth/login` - Handle user login.

#### Admin Routes
- `GET /admin_dashboard` - Admin dashboard with all orders (admin authentication required).
- `POST /admin/cancel_orders` - Cancel all orders for a specific user (admin authentication required).

#### Pizza Routes
- `GET /api/pizzas` - Retrieve list of pizzas (user authentication required).

#### Order Routes
- `POST /api/orders` - Create a new order (user authentication required).
- `PUT /api/orders/{order_id}` - Update an existing order (user authentication required).
- `DELETE /api/orders/{order_id}` - Delete an order (user authentication required).
- `GET /api/orders/{user_id}` - Retrieve orders for a specific user (authentication and authorization required).

### 💾 Local Storage
- Maintain cart state using local storage.
- Ensure cart persists across page reloads.

### 💻 Frontend
- Responsive UI for pizzas and cart contents.
- Interactive elements for cart management.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI
- **Database**: MongoDB
- **Session Management**: FastAPI-integrated

## Setup and Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/missLaiba22/Pizza-Delivery-App
    cd joeys-pizza-delivery
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the FastAPI application**:
    ```bash
    uvicorn main:app --reload
    ```

5. **Access the application**:
    Open your web browser and navigate to `http://127.0.0.1:8000`.

## Summary

Joey's Pizza Delivery app is a full-featured pizza ordering platform offering a seamless user experience from browsing to ordering, with robust admin tools for managing orders. 🍕🚀
