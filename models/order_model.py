from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from models.base_model import Base
from utils.uuid_generate import generate_uuid


# Creating Order model
class Order(Base):
    """Represents customer orders in the jewelry system."""

    __tablename__ = "orders"

    id = Column(String(60), primary_key=True, default=generate_uuid)
    customer_id = Column(String(60),ForeignKey("customers.id"),nullable=False)
    order_date = Column(DateTime,default=lambda: datetime.now(timezone.utc))
    status = Column(String(50),nullable=False)
    total_amount = Column(Numeric(10, 2),nullable=False)


    # Creating relationship with Customer model
    customer = relationship("Customer",back_populates="orders")

    # Defining relationship between Order and OrderItem
    items = relationship("OrderItem",back_populates="order")


    def __str__(self):
        return f"Order(id={self.id}, status={self.status})"


    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "order_date": self.order_date,
            "status": self.status,
            "total_amount": self.total_amount
        }