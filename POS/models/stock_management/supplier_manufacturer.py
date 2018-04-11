from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from POS.models.base_model import AppDB


class SupplierManufacturer(AppDB.BaseModel):
    """
        Link model for the supplier and manufacturer model
    """
    __tablename__ = "supplier_manufacturer"

    supplier_id = Column(Integer, ForeignKey("supplier.id"), primary_key=True)
    manufacturer_id = Column(Integer, ForeignKey("manufacturer.id"), primary_key=True)

    # Relationship
    supplier = relationship("Supplier", back_populates="manufacturers")
    manufacturer = relationship("Manufacturer", back_populates="suppliers")

    def __init__(self, supplier_id, manufacturer_id):
        self.supplier_id = supplier_id
        self.manufacturer_id = manufacturer_id

    def __repr__(self):
        return "SupplierManufacturer<supplier_id={0}, manufacturer_id={1}>".format(
            self.supplier_id,
            self.manufacturer_id
        )
