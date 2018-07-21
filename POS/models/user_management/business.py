from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from POS.models.base_model import AppDB


class Business(AppDB.BaseModel):
    """
        Represents a Lipa Less Business
    """
    __tablename__ = "business"

    # Attributes
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_number = Column(String)

    # Relationships
    users = relationship("UserBusiness", back_populates="business")
    products = relationship("Product", back_populates="business")
    categories = relationship("Category", back_populates="business")
    ewallet = relationship("EWallet", back_populates = "business")
    sales_transactions = relationship("SalesTransaction", back_populates="business")

    def __init__(self, name, contact_no):
        self.name = name
        self.contact_number = contact_no

    def __repr__(self):
        return "Business<name=%s, contact_number=%s>" % (
            self.name,
            self.contact_number
        )

    @staticmethod
    def exists(business_id):
        return AppDB.db_session.query(Business).filter(
            Business.id == business_id
        ).first()
