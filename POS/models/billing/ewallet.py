import random

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from POS import constants
from POS.models.base_model import AppDB


class EWallet(AppDB.BaseModel):
    """
        Represents a Lipa Less Business
    """
    __tablename__ = "ewallet"

    # Attributes
    account_id = Column(Integer, primary_key=True)
    balance = Column(Integer)
    business_id = Column(Integer, ForeignKey("business.id"), primary_key=True)

    # Relationships
    business = relationship("Business", back_populates="ewallet")

    def __init__(self, balance=0):
        # Keep generating random account IDs while making sure they are unique
        unique_account_id = constants.MINIMUM_PAYMENT_ID + \
                          (random.random() * constants.MAXIMUM_PAYMENT_ID)
        while EWallet.exists(unique_account_id):
            unique_account_id = constants.MINIMUM_PAYMENT_ID + \
                              (random.random() * constants.MAXIMUM_PAYMENT_ID)

        self.account_id = unique_account_id
        self.balance = balance

    def __repr__(self):
        return "EWallet<account_id=%s, balance=%s>" % (
            self.account_id,
            self.balance
        )

    @staticmethod
    def exists(account_id):
        return AppDB.db_session.query(EWallet).filter(
            EWallet.account_id == account_id
        ).first()
