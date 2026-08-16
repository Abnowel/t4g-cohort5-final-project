from fastapi import FastAPI
from routes.customer_route import router as customer_router
from routes.jewelry_route import router as jewelry_router
from routes.order_route import router as order_router
from routes.order_item_route import router as order_item_router
from fastapi.staticfiles import StaticFiles

# Create our FastAPI application
app = FastAPI()

# Register customer routes with the main application
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
app.include_router(customer_router)
app.include_router(jewelry_router)
app.include_router(order_router)
app.include_router(order_item_router)



# Our first API endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to the Jewelry Order and Inventory Management System"
    }

