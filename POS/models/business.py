from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class Business(BaseModel):
    """
        Represents a Lipa Less Business
    """
    __tablename__ = "business"

    # Attributes
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_number = Column(String)

    users = relationship(
        "UserBusiness",
        back_populates="business"
    )

    def __init__(self, name, contact_no):
        self.name = name
        self.contact_number = contact_no

    def __repr__(self):
        return "Business<name=%s, contact_number=%s>" % (
            self.name,
            self.contact_number
        )
