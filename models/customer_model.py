from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base
from utils.uuid_generate import generate_uuid

# Creating Customer model
class Customer(Base):
    """Represents a customer in the jewelry system."""

    __tablename__ = "customers"

    id = Column(String(60), primary_key=True, default=generate_uuid)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(10), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    address = Column(String(150), nullable=False)

    # Creating relationship with Order model
    orders = relationship("Order",back_populates="customer")


    def __str__(self):
        return(
            f"Customer(id={self.id}, Name ={self.first_name} {self.last_name})"
            )

    def to_dict(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": self.address,
            }