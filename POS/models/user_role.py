from sqlalchemy import Column, Integer

from POS.models.base_model import BaseModel


class UserRole(BaseModel):
    """
        Represents the various roles played by users
    """
    __tablename__ = "user_role"

    # Attributes
    emp_id = Column(Integer, primary_key=True)
    role_id = Column(Integer, nullable=False)

    def __init__(self, emp_id, role_id):
        self.emp_id = emp_id
        self.role_id = role_id

    def __repr__(self):
        return "UserRole<emp_id=%s, role_id=%s>" % (
            self.emp_id,
            self.role_id
        )
