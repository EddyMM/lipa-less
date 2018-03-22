"""
    This module uses SQLAlchemy to create the database structures (if they do not exist)
    and exposes a database session object to be used by the app
"""

from flask import logging, current_app

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..constants import DATABASE_URL_ENV_NAME


class AppDB(object):
    # Create the BaseModel model through which all other models will be declared
    BaseModel = declarative_base()
    db_session = None

    @staticmethod
    def init_db():
        # Import the various models
        # noinspection PyUnresolvedReferences
        from .user import User
        # noinspection PyUnresolvedReferences
        from .business import Business
        # noinspection PyUnresolvedReferences
        from .role import Role
        # noinspection PyUnresolvedReferences
        from .user_business import UserBusiness

        try:
            db_engine = create_engine(current_app.config["SQLALCHEMY_DATABASE_URI"])

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
            logger = logging.getLogger()
            logger.log(
                logging.ERROR,
                "%s attribute not found or provided" % DATABASE_URL_ENV_NAME
            )
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
