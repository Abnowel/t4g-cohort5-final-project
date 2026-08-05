from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import Base
from utils.uuid_generate import generate_uuid


# Creating OrderItem model
class OrderItem(Base):
    """Represents items inside a customer's order."""

    __tablename__ = "order_items"

    id = Column(String(60), primary_key=True, default=generate_uuid)
    order_id = Column(String(60),ForeignKey("orders.id"),nullable=False)
    jewelry_id = Column(String(60),ForeignKey("jewelry.id"),nullable=False)
    quantity = Column(Integer,nullable=False)
    price = Column(Numeric(10, 2),nullable=False)

    # Defining relationships between OrderItem, Order, and Jewelry
    
    order = relationship("Order",back_populates="items")

    jewelry = relationship("Jewelry",back_populates="order_items")


    def __str__(self):
        return f"OrderItem(id={self.id}, quantity={self.quantity})"


    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "jewelry_id": self.jewelry_id,
            "quantity": self.quantity,
            "price": self.price
        }