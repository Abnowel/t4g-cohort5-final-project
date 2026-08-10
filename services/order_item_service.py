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


    # Get all order items
    def get_all_order_items(self):
        order_items = self.session.query(OrderItem).all()

        return order_items

    # Get one order item by ID
    def get_order_item_by_id(self, order_item_id):

        order_item = self.session.query(OrderItem).filter(
            OrderItem.id == order_item_id
        ).first()

        return order_item

    # Update an existing order item
    def update_order_item(self, order_item_id, order_item_data):

        order_item = self.session.query(OrderItem).filter(
            OrderItem.id == order_item_id
        ).first()

        if order_item is None:
            return None

        if order_item_data.get("order_id") is not None:
            order_item.order_id = order_item_data.get("order_id")

        if order_item_data.get("jewelry_id") is not None:

            jewelry = self.session.query(Jewelry).filter(
                Jewelry.id == order_item_data.get("jewelry_id")
            ).first()

            if jewelry is None:
                return None

            order_item.jewelry_id = order_item_data.get("jewelry_id")
            order_item.price = jewelry.price

        if order_item_data.get("quantity") is not None:
            order_item.quantity = order_item_data.get("quantity")

        self.session.commit()

        return order_item

    # Delete an existing order item
    def delete_order_item(self, order_item_id):

        order_item = self.session.query(OrderItem).filter(
            OrderItem.id == order_item_id
        ).first()

        if order_item is None:
            return None

        self.session.delete(order_item)
        self.session.commit()

        return order_item

    