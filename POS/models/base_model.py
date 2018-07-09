"""
    This module uses SQLAlchemy to create the database structures (if they do not exist)
    and exposes a database session object to be used by the app
"""

from flask import current_app

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class AppDB(object):
    # Create the BaseModel model through which all other models will be declared
    BaseModel = declarative_base()
    db_session = None

    # noinspection PyUnresolvedReferences
    @staticmethod
    def init_db():
        # Import the various models
        from POS.models.user_management.user import User
        from POS.models.user_management.business import Business
        from POS.models.user_management.role import Role
        from POS.models.user_management.user_business import UserBusiness
        from POS.models.stock_management.category import Category
        from POS.models.stock_management.supplier import Supplier
        from POS.models.stock_management.manufacturer import Manufacturer
        from POS.models.stock_management.product import Product
        from POS.models.stock_management.supplier_manufacturer import SupplierManufacturer
        from POS.models.billing.ewallet import EWallet
        from POS.models.billing.billing_transaction import BillingTransaction

        try:
            db_engine = create_engine(
                current_app.config["SQLALCHEMY_DATABASE_URI"],
                isolation_level='READ COMMITTED'
            )

            # Bind the engine to the models
            AppDB.BaseModel.metadata.bind = db_engine

            # Create a session object to be used by the app to do any DB transaction
            # noinspection PyPep8Naming
            Session = sessionmaker(
                bind=db_engine
            )

            AppDB.db_session = Session()

            # Create all structures
            # AppDB.BaseModel.metadata.drop_all()
            AppDB.BaseModel.metadata.create_all()

            # Load default user roles
            AppDB.load_default_roles(Role)

        except AttributeError:
            current_app.logger.error("Database URL attribute not found or provided")
            raise

    # noinspection PyPep8Naming
    @staticmethod
    def load_default_roles(Role):
        default_roles = Role.load_roles_from_config()

        for role_id, role in default_roles.items():
            role_name = role["name"]
            role_description = role["description"]

            # Check if role already exists
            existing_role = AppDB.db_session.query(Role).filter(
                Role.name == role_name
            ).first()

            # If it doesn't create it
            if not existing_role:
                role = Role(role_name, role_description)
                AppDB.db_session.add(role)
                AppDB.db_session.commit()
