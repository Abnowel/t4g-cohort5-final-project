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

    def get_all_customers(self):
         customers = self.session.query(Customer).all()
         return customers

    def get_customer_by_id(self, customer_id):
        return self.session.query(Customer).filter(Customer.id == customer_id).first()


    def update_customer(self, customer_id, customer_data):
        customer = self.session.query(Customer).filter(Customer.id == customer_id).first()

        if customer is None:
            return None

        customer.first_name = customer_data.get("first_name", customer.first_name)
        customer.last_name = customer_data.get("last_name", customer.last_name)
        customer.phone_number = customer_data.get("phone_number", customer.phone_number)
        customer.email = customer_data.get("email", customer.email)
        customer.address = customer_data.get("address", customer.address)

        self.session.commit()

        return customer

    def delete_customer(self, customer_id):
        customer = self.session.query(Customer).filter(Customer.id == customer_id).first()

        if customer is None:
            return None

        self.session.delete(customer)
        self.session.commit()

        return customer