import os

from flask import session, redirect, url_for
from flask_login import current_user

from POS.models.base_model import AppDB
from POS.models.user_management.user_business import UserBusiness
from POS.models.user_management.role import Role

from .constants import APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR, OWNER_ROLE_NAME, ADMIN_ROLE_NAME, CASHIER_ROLE_NAME


def get_config_type():
    return os.environ.get(APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR).lower().strip()


def selected_business(business_dependent_func):
    """
        Decorator function that checks if the user has already selected a business
    :return:
    """
    def wrapper(*args, **kwargs):
        if not session.get("business_id"):
            return redirect(
                location=url_for("business_bp.business"),
                code=303
            )
        return business_dependent_func(*args, **kwargs)
    return wrapper


def is_owner(owner_restricted_func):
    """
    Decorator func to check if the user is the owner before executing a function
    :param owner_restricted_func:
    :return:
    """

    @selected_business
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


def is_admin(admin_restricted_func):
    """
        Decorator func to check if the user is the owner before executing a function
        :param admin_restricted_func:
        :return:
        """

    @selected_business
    def wrapper(*args, **kwargs):
        # Check if current user is an admin or owner of the current business
        # (since what an admin can do, an owner can as well)
        # N/B: I know that the above statement looks like inheritance but
        # the roles themselves are not purely associated with a User
        # rather it's an attribute of the User and the Business so inheritance concept is not being applied

        # First get the admin role
        admin_role = AppDB.db_session.query(Role).filter(
            Role.name == ADMIN_ROLE_NAME
        ).first()

        admin = AppDB.db_session.query(UserBusiness).get((
            current_user.emp_id,
            session.get("business_id"),
            admin_role.id)
        )

        owner_role = AppDB.db_session.query(Role).filter(
            Role.name == OWNER_ROLE_NAME
        ).first()

        owner = AppDB.db_session.query(UserBusiness).get((
            current_user.emp_id,
            session.get("business_id"),
            owner_role.id)
        )

        if not admin and not owner:
            return redirect(
                location=url_for("business_bp.business"),
                code=303
            )
        return admin_restricted_func(*args, **kwargs)

    return wrapper


def is_cashier(cashier_restricted_func):
    """
            Decorator func to check if the user is the owner before executing a function
            :param cashier_restricted_func:
            :return:
            """

    @selected_business
    def wrapper():
        # Check if current user is an admin or owner of the current business
        # (since what an admin can do, an owner can as well)
        # N/B: I know that the above statement looks like inheritance but
        # the roles themselves are not purely associated with a User
        # rather it's an attribute of the User and the Business so inheritance concept is not being applied

        # First get the owner role
        owner_role = AppDB.db_session.query(Role).filter(
            Role.name == OWNER_ROLE_NAME
        ).first()

        owner = AppDB.db_session.query(UserBusiness).get((
            current_user.emp_id,
            session.get("business_id"),
            owner_role.id)
        )

        # Then the admin role
        admin_role = AppDB.db_session.query(Role).filter(
            Role.name == ADMIN_ROLE_NAME
        ).first()

        admin = AppDB.db_session.query(UserBusiness).get((
            current_user.emp_id,
            session.get("business_id"),
            admin_role.id)
        )

        # Then the cashier role
        cashier_role = AppDB.db_session.query(Role).filter(
            Role.name == CASHIER_ROLE_NAME
        ).first()

        cashier = AppDB.db_session.query(UserBusiness).get((
            current_user.emp_id,
            session.get("business_id"),
            cashier_role.id)
        )

        if not admin and not owner and not cashier:
            return redirect(
                location=url_for("business_bp.business"),
                code=303
            )
        return cashier_restricted_func()

    return wrapper
