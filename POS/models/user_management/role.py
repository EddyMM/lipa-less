import os

import yaml
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from flask import logging

from POS.models.base_model import AppDB
from POS.constants import ROLES_YAML_ENV_VAR, CASHIER_ROLE_NAME


class Role(AppDB.BaseModel):
    """
        Represents the various roles played by users
    """
    __tablename__ = "role"

    # Attributes
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    user_businesses = relationship(
        "UserBusiness",
        back_populates="role"
    )

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "Role<name=%s>" % (
            self.name
        )

    @staticmethod
    def load_roles_from_config():
        local_roles_yaml_path = os.environ.get(ROLES_YAML_ENV_VAR)

        roles = Role.get_dict_from_yaml(local_roles_yaml_path)

        if not roles:
            logging.getLogger().log(
                logging.ERROR,
                "ROLES_YAML_PATH not specified, trying to load from in-app config"
            )

            in_app_roles_yaml_path = "POS/config/roles.yaml"
            roles = Role.get_dict_from_yaml(in_app_roles_yaml_path)
        return roles

    @staticmethod
    def get_dict_from_yaml(yaml_path):
        if yaml_path and os.path.exists(yaml_path):
            with open(yaml_path, "rb") as roles_yaml:
                return yaml.load(roles_yaml)
        return None

    @staticmethod
    def get_role_id(role_name=CASHIER_ROLE_NAME):
        owner_role = AppDB.db_session.query(Role).filter(
            Role.name == role_name
        ).first()
        if owner_role:
            return owner_role.id
        return None
