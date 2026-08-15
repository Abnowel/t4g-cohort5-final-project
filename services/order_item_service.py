from models.order_item_model import OrderItem
from models.jewelry_model import Jewelry
from models.order_model import Order
from utils.database_connection import db_session


class OrderItemService:
    """Creating OrderItemService to handle order item database operations"""
    def __init__(self, session=db_session):
        self.session = session

    # Create a new order item
    def create_order_item(self, order_item_data):

        # Check if the order exists
        order = self.session.query(Order).filter(
            Order.id == order_item_data.get("order_id")
        ).first()

        if order is None:
            return "order_not_found"

        # Check if the jewelry exists
        jewelry = self.session.query(Jewelry).filter(
            Jewelry.id == order_item_data.get("jewelry_id")
        ).first()

        if jewelry is None:
            return "jewelry_not_found"

        quantity = order_item_data.get("quantity")

        # Check if there is enough stock
        if quantity > jewelry.stock_quantity:
            return "insufficient_stock"
        
        new_order_item = OrderItem(
            order_id=order_item_data.get("order_id"),
            jewelry_id=order_item_data.get("jewelry_id"),
            quantity=order_item_data.get("quantity"),
            price=jewelry.price
        )
        self.session.add(new_order_item)
       

        # Reduce availabel stock
        jewelry.stock_quantity -= quantity

        self.session.commit()

        # Recalculate the order total
        self.recalculate_order_total(new_order_item.order_id)

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

        old_jewelry = self.session.query(Jewelry).filter(
            Jewelry.id == order_item.jewelry_id
        ).first()

        old_quantity = order_item.quantity

        new_jewelry = old_jewelry

        # Check if the jewelry is being changed
        if order_item_data.get("jewelry_id") is not None:

            new_jewelry = self.session.query(Jewelry).filter(
                Jewelry.id == order_item_data.get("jewelry_id")
            ).first()

            if new_jewelry is None:
                return None

        # Get the new quantity
        new_quantity = order_item_data.get(
            "quantity",
            old_quantity
        )

        # If jewelry is being changed
        if new_jewelry.id != old_jewelry.id:

            # Check if the new jewelry has enough stock
            if new_quantity > new_jewelry.stock_quantity:
                return "insufficient_stock"

            # Return old quantity to old jewelry
            old_jewelry.stock_quantity += old_quantity

            # Remove new quantity from new jewelry
            new_jewelry.stock_quantity -= new_quantity

            # Update jewelry and price
            order_item.jewelry_id = new_jewelry.id
            order_item.price = new_jewelry.price

        else:

            # Jewelry is not changing
            difference = new_quantity - old_quantity

            # Increasing quantity
            if difference > 0:

                if difference > new_jewelry.stock_quantity:
                    return "insufficient_stock"

                new_jewelry.stock_quantity -= difference

            # Decreasing quantity
            elif difference < 0:

                new_jewelry.stock_quantity += abs(difference)

        # Update the quantity
        order_item.quantity = new_quantity

        try:
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

        # Recalculate the order total
        self.recalculate_order_total(order_item.order_id)

        return order_item

    # Delete an existing order item
    def delete_order_item(self, order_item_id):

        order_item = self.session.query(OrderItem).filter(
            OrderItem.id == order_item_id
        ).first()

        if order_item is None:
            return None

        jewelry = self.session.query(Jewelry).filter(
            Jewelry.id == order_item.jewelry_id
        ).first()

        order_id = order_item.order_id

        # Return the quantity to stock
        if jewelry is not None:
            jewelry.stock_quantity += order_item.quantity


        self.session.delete(order_item)
        self.session.commit()

        # Recalculate the order total
        self.recalculate_order_total(order_id)

        return order_item

    # Recalculate the total amount of an order
    def recalculate_order_total(self, order_id):

        order_items = self.session.query(OrderItem).filter(
        OrderItem.order_id == order_id
        ).all()

        total = sum(
            order_item.price * order_item.quantity
            for order_item in order_items
        )

        order = self.session.query(Order).filter(
            Order.id == order_id
        ).first()

        if order is not None:
            order.total_amount = total
            self.session.commit()

    