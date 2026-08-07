from models.jewelry_model import Jewelry
from utils.database_connection import db_session


class JewelryService:
    def __init__(self, session=db_session):
        self.session = session

    # Creating a new jewelry item
    def create_jewelry(self, jewelry_data):
        new_jewelry = Jewelry(
        name=jewelry_data.get("name"),
        category=jewelry_data.get("category"),
        material=jewelry_data.get("material"),
        price=jewelry_data.get("price"),
        stock_quantity=jewelry_data.get("stock_quantity")
    )

        self.session.add(new_jewelry)
        self.session.commit()

        return new_jewelry

    # Get all jewelry items
    def get_all_jewelry(self):
        jewelry = self.session.query(Jewelry).all()

        return jewelry
    
    # Get one jewelry item by ID
    def get_jewelry_by_id(self, jewelry_id):
        jewelry = self.session.query(Jewelry).filter(Jewelry.id == jewelry_id).first()

        return jewelry

    # Update a jewelry item
    def update_jewelry(self, jewelry_id, jewelry_data):
        jewelry = self.session.query(Jewelry).filter(
        Jewelry.id == jewelry_id
    ).first()

        if jewelry is None:
            return None

        jewelry.name = jewelry_data.get("name", jewelry.name)
        jewelry.category = jewelry_data.get("category", jewelry.category)
        jewelry.material = jewelry_data.get("material", jewelry.material)
        jewelry.price = jewelry_data.get("price", jewelry.price)
        jewelry.stock_quantity = jewelry_data.get(
        "stock_quantity",
        jewelry.stock_quantity
    )

        self.session.commit()

        return jewelry

    # Delete a jewelry item
    def delete_jewelry(self, jewelry_id):
        jewelry = self.session.query(Jewelry).filter(
        Jewelry.id == jewelry_id
    ).first()

        if jewelry is None:
            return None

        self.session.delete(jewelry)
        self.session.commit()

        return jewelry