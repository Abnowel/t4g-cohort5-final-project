from models.customer_model import Customer
from utils.database_connection import db_session

class CustomerService:
    """Handles all customer-related database operations."""
    def __init__(self, session=db_session):
        self.session = session

    def create_customer(self, customer_data):
        customer = Customer(
    first_name=customer_data.get("first_name"),
    last_name=customer_data.get("last_name"),
    phone_number=customer_data.get("phone_number"),
    email=customer_data.get("email"),
    address=customer_data.get("address")
)
        self.session.add(customer)
        self.session.commit()

        return customer