from fastapi import FastAPI
from routes.customer_route import router as customer_router

# Create our FastAPI application
app = FastAPI()

# Register customer routes with the main application
app.include_router(customer_router)


# Our first API endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to the Jewelry Order and Inventory Management System"
    }

