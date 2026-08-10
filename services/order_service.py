from models.order_model import Order
from utils.database_connection import db_session


class OrderService:
    """ Creating OrderService to handle order database operations"""
    def __init__(self, session=db_session):
        self.session = session

    # Creating a new order
    def create_order(self, order_data):

        new_order = Order(
        customer_id=order_data.get("customer_id"),
        status=order_data.get("status"),
        total_amount=order_data.get("total_amount")
    )

        self.session.add(new_order)
        self.session.commit()

        return new_order

    # Get all orders
    def get_all_orders(self):
        orders = self.session.query(Order).all()

        return orders

    # Get one order by ID
    def get_order_by_id(self, order_id):
        order = self.session.query(Order).filter(
        Order.id == order_id
    ).first()

        return order
        