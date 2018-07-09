import datetime

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from POS.models.base_model import AppDB


class BillingTransaction(AppDB.BaseModel):
    """
        Represents a Lipa Less Business
    """
    __tablename__ = "billing_transaction"

    # Attributes
    transaction_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    amount = Column(Float)
    account_id = Column(Integer, ForeignKey("ewallet.account_id"))

    # Relationships
    ewallet = relationship("EWallet", back_populates="billing_transactions")

    def __init__(self, amount=0):
        self.timestamp = datetime.datetime.now()
        self.amount = amount

    def __repr__(self):
        return "Transaction<transaction_id=%s, amount=%s>" % (
            self.account_id,
            self.amount
        )

    @staticmethod
    def exists(account_id):
        return AppDB.db_session.query(BillingTransaction).filter(
            BillingTransaction.account_id == account_id
        ).first()
