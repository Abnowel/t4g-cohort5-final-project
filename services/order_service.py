from models.order_model import Order
from models.order_item_model import OrderItem
from models.jewelry_model import Jewelry
from models.customer_model import Customer
from sqlalchemy.exc import IntegrityError
from utils.database_connection import db_session


class OrderService:
    """ Creating OrderService to handle order database operations"""
    def __init__(self, session=db_session):
        self.session = session

    # Creating a new order
    def create_order(self, order_data):
        customer = self.session.query(Customer).filter(
        Customer.id == order_data.get("customer_id")
    ).first()

        if customer is None:
            return "customer_not_found"
        items = order_data.get("items",[])

        # Checking that all jewelry items exist before creating the order
        jewelry_items = []

        for item in items:
            jewelry = self.session.query(Jewelry).filter(
                Jewelry.id == item.get("jewelry_id")
            ).first()

            if jewelry is None:
                return None

            jewelry_items.append(
                (item,jewelry)
            )

        new_order = Order(
            customer_id=order_data.get("customer_id"),
            status="pending",
            total_amount=0
        )

        self.session.add(new_order)
        self.session.flush()

        total = 0

        # Creating order items for the new order
        for item ,jewelry in jewelry_items:

            order_item = OrderItem(
                order_id = new_order.id,
                jewelry_id = jewelry.id,
                quantity = item.get("quantity"),
                price = jewelry.price
            )

            self.session.add(order_item)

            total += jewelry.price * item.get("quantity")

        # Setting the calculated order total
        new_order.total_amount = total

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

    # Update an existing order
    def update_order(self, order_id, order_data):

        order = self.session.query(Order).filter(
        Order.id == order_id
        ).first()

        if order is None:
            return None

        if order_data.get("status") is not None:
            order.status = order_data.get("status")
        

        self.session.commit()

        return order 

    # Delete an existing order
    def delete_order(self, order_id):
        order = self.session.query(Order).filter(
        Order.id == order_id
        ).first()

        if order is None:
            return None

        try:
            self.session.delete(order)
            self.session.commit()
            
        except IntegrityError:
            self.session.rollback()
            return "has_order_items"

        return order

    # Calculate the total amount of an order
    def calculate_order_total(self, order_id):

        order_items = self.session.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).all()

        total = sum(
            item.price * item.quantity
            for item in order_items
        )

        return total  