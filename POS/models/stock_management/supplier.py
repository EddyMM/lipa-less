from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from POS.models.base_model import AppDB


class Supplier(AppDB.BaseModel):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_person = Column(String)
    contact_no = Column(String)

    # Relationships
    products = relationship("Product", back_populates="supplier")
    manufacturers = relationship("SupplierManufacturer", back_populates="supplier")

    def __init__(self, name, contact_person, contact_no):
        self.name = name
        self.contact_person = contact_person
        self.contact_no = contact_no

    def __repr__(self):
        return "Supplier<name={0}, contact_person={1}, contact_no={2}>".format(
            self.name,
            self.contact_person,
            self.contact_no
        )
