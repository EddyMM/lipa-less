from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin

from .base_model import BaseModel


class User(BaseModel, UserMixin):
    """
        Represents a Lipa Less User, may be an owner, admin or cashier
    """
    __tablename__ = "lipalessuser"

    # Attributes
    emp_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    # Specify relationships
    businesses = relationship(
        "UserBusiness",
        back_populates="user"
    )

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return "User<name=%s, email=%s>" % (
            self.name,
            self.email
        )

    def get_id(self):
        return self.emp_id

    def confirm_password(self, proposed_password):
        """
        Checks if a provided password is the correct user's password
        :param proposed_password: Provided password by user
        :return: True is the password is correct, False otherwise
        """
        return check_password_hash(
            pwhash=self.password,
            password=proposed_password
        )
