import os

from flask import session, redirect, url_for
from flask_login import current_user

from POS.models.base_model import AppDB
from POS.models.user_business import UserBusiness
from POS.models.role import Role

from .constants import APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR, OWNER_ROLE_NAME


def get_config_type():
    return os.environ.get(APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR).lower().strip()


def selected_business(business_dependent_func):
    """
        Decorator function that checks if the user has already selected a business
    :return:
    """
    def wrapper():
        if not session.get("business_id"):
            return redirect(
                location="/business",
                code=303
            )
        return business_dependent_func()
    return wrapper


def is_owner(owner_restricted_func):
    """
    Decorator func to check if the user is the owner before executing a function
    :param owner_restricted_func:
    :return:
    """
    def wrapper():
        # Check if current user os an owner of the current business
        # First get the owner role id
        owner_role = AppDB.db_session.query(Role).filter(
            Role.name == OWNER_ROLE_NAME
        ).first()

        owner = AppDB.db_session.query(UserBusiness).get((
            current_user.emp_id,
            session.get("business_id"),
            owner_role.id)
        )

        if not owner:
            return redirect(
                location=url_for("business_bp.business"),
                code=303
            )
        return owner_restricted_func()

    return wrapper
