from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from POS.models.base_model import AppDB


class UserBusiness(AppDB.BaseModel):
    """
        Association model for the User and Business models
    """
    __tablename__ = "user_business"

    emp_id = Column(Integer, ForeignKey("lipalessuser.emp_id"), primary_key=True)
    business_id = Column(Integer, ForeignKey("business.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"), primary_key=True)
    is_deactivated = Column(Boolean, nullable=False)

    user = relationship(
        "User",
        back_populates="businesses"
    )
    business = relationship(
        "Business",
        back_populates="users"
    )
    role = relationship(
        "Role",
        back_populates="user_businesses"
    )

    def __init__(self, role_id, is_deactivated=False):
        self.role_id = role_id
        self.is_deactivated = is_deactivated

    def __repr__(self):
        return "UserBusiness<emp_id={0}, business_id={1}, role_id={2}, is_deactivated={3}>".format(
            self.emp_id,
            self.business_id,
            self.role_id,
            self.is_deactivated
        )
