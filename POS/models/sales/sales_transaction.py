from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from POS.models.base_model import AppDB


class SalesTransaction(AppDB.BaseModel):
    __tablename__ = "sales_transaction"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    amount_given = Column(Float, nullable=False)

    # Foreign fields
    cashier_id = Column(Integer, ForeignKey("lipalessuser.emp_id"), nullable=False)
    business_id = Column(Integer, ForeignKey("business.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="sales_transactions")
    business = relationship("Business", back_populates="sales_transactions")
    line_items = relationship("LineItem", back_populates="sales_transaction")

    def __init__(self, timestamp, amount_given):
        self.timestamp = timestamp
        self.amount_given = amount_given

    def __repr__(self):
        return "SalesTransaction<id={0}, timestamp={1}>".format(
            self.id, self.timestamp
        )
