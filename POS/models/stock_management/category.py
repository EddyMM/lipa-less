from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from POS.models.base_model import AppDB


class Category(AppDB.BaseModel):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    # Foreign fields
    business_id = Column(Integer, ForeignKey("business.id"), nullable=False)

    # Relationships
    products = relationship("Product", back_populates="category")
    business = relationship("Business", back_populates="categories")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "Category<name={}>".format(
            self.name,
        )
