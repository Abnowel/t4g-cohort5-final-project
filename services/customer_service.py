from models.customer_model import Customer
from utils.database_connection import db_session

class CustomerService:
    """Handles all customer-related database operations."""
    def __init__(self, session=db_session):
        self.session = session

    def create_customer(self, customer_data):
        