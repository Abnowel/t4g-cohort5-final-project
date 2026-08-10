from models.order_item_model import OrderItem
from models.jewelry_model import Jewelry
from utils.database_connection import db_session


class OrderItemService:
    """Creating OrderItemService to handle order item database operations"""
    def __init__(self, session=db_session):
        self.session = session

    # Create a new order item
    def create_order_item(self, order_item_data):

        jewelry = self.session.query(Jewelry).filter(
            Jewelry.id == order_item_data.get("jewelry_id")
        ).first()

        if jewelry is None:
            return None

        new_order_item = OrderItem(
            order_id=order_item_data.get("order_id"),
            jewelry_id=order_item_data.get("jewelry_id"),
            quantity=order_item_data.get("quantity"),
            price=jewelry.price
        )

        self.session.add(new_order_item)
        self.session.commit()

        return new_order_item


    

    