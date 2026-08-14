from sqlalchemy import Column, String, Numeric, Integer
from sqlalchemy.orm import relationship
from models.base_model import Base
from utils.uuid_generate import generate_uuid


# Creating Jewelry model
class Jewelry(Base):
    """Represents jewelry products in the system."""

    __tablename__ = "jewelry"

    id = Column(String(60), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=False)
    material = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    # Defining relationship between Jewelry and OrderItem
    order_items = relationship("OrderItem",back_populates="jewelry")

    def __str__(self):
        return (
            f"Jewelry(id={self.id}, name={self.name}, price=GHS {self.price})"
            )


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "material": self.material,
            "price": f"GHS {self.price}",
            "stock_quantity": self.stock_quantity
            }