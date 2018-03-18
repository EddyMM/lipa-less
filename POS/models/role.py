from sqlalchemy import Column, Integer, String

from .base_model import BaseModel


class Role(BaseModel):
    """
        Represents the various roles played by users
    """
    __tablename__ = "role"

    # Attributes
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "Role<name=%s>" % (
            self.name
        )
