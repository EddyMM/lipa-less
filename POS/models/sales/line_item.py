from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from POS.models.base_model import AppDB


class LineItem(AppDB.BaseModel):
    __tablename__ = "line_item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    # Foreign fields
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    sales_transaction_id = Column(Integer, ForeignKey("sales_transaction.id"), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="line_item")
    sales_transaction = relationship("SalesTransaction", back_populates="line_items")

    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return "LineItem<name={0}, price={1}, quantity={2}, product_id={3}>".format(
            self.name, self.price, self.quantity, self.product_id
        )
