from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from POS.models.base_model import AppDB


class Manufacturer(AppDB.BaseModel):
    __tablename__ = "manufacturer"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationships
    # products = relationship("Product", back_populates="manufacturer")
    # suppliers = relationship("SupplierManufacturer", back_populates="manufacturer")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Manufacturer<name={}>".format(
            self.name,
        )
