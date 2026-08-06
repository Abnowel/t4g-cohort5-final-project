from fastapi import FastAPI


# Create our FastAPI application
app = FastAPI()


# Our first API endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to the Jewelry Order and Inventory Management System"
    }

