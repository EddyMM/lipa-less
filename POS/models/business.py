from sqlalchemy import Column, Integer, String, ForeignKey

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
    emp_id = Column(
        Integer,
        ForeignKey("lipalessuser.emp_id")
    )

    def __init__(self, name, contact_no, emp_id):
        self.name = name
        self.contact_number = contact_no
        self.emp_id = emp_id

    def __repr__(self):
        return "Business<name=%s, contact_number=%s>" % (
            self.name,
            self.contact_number
        )
