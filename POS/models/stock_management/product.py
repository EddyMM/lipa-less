from POS.models.base_model import AppDB

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship


class Product(AppDB.BaseModel):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    buying_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    reorder_level = Column(Integer)
    expiration_date = Column(Date)
    quantity = Column(Integer, nullable=False)
    # Foreign keys
    business_id = Column(Integer, ForeignKey("business.id"))
    category_id = Column(Integer, ForeignKey("category.id"))
    # supplier_id = Column(Integer, ForeignKey("supplier.id"))
    # manufacturer_id = Column(Integer, ForeignKey("manufacturer.id"))

    # Relationships
    business = relationship("Business", back_populates="products")
    category = relationship("Category", back_populates="products")
    # supplier = relationship("Supplier", back_populates="products")
    # manufacturer = relationship("Manufacturer", back_populates="products")

    def __init__(self, name, description, buying_price, selling_price, reorder_level,
                 expiration_date, quantity):
        self.name = name
        self.description = description
        self.buying_price = buying_price
        self.selling_price = selling_price
        self.reorder_level = reorder_level
        self.expiration_date = expiration_date
        self.quantity = quantity

    def __repr__(self):
        return "Product<name={}, selling_price={}, quantity={}>".format(
            self.name, self.selling_price, self.quantity
        )
