import yaml
from sqlalchemy import Column, Integer, String

from POS.models.base_model import BaseModel


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

    @staticmethod
    def load_roles_from_config():
        with open("POS/config/roles.yaml", "rb") as roles_yaml:
            return yaml.load(roles_yaml)
