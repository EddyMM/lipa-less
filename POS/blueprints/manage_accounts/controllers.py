from flask import Blueprint, render_template, request, session, current_app
from flask_login import login_required, current_user

from sqlalchemy.exc import SQLAlchemyError

from POS.blueprints.base.app_view import AppView
from POS.models.base_model import AppDB
from POS.models.user_management.user import User
from POS.models.user_management.business import Business
from POS.models.user_management.role import Role
from POS.models.user_management.user_business import UserBusiness

from POS.constants import APP_NAME, OWNER_ROLE_NAME, ADMIN_ROLE_NAME
from POS.utils import is_admin


class ManageAccountsAPI(AppView):
    @staticmethod
    @login_required
    @is_admin
    def get():
        try:
            # Get a list of all the user accounts in the business
            accounts = ManageAccountsAPI.get_all_accounts()

            # Get a list of all possible roles in the business so
            # that the owner or admin can select from a variety or roles
            roles = ManageAccountsAPI.get_all_roles()

            # noinspection PyUnresolvedReferences
            return render_template(
                template_name_or_list="manage_accounts.html",
                title="%s: %s" % (APP_NAME, "Accounts"),
                accounts=accounts,
                roles=roles
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return ManageAccountsAPI.error_in_processing_request()

    @staticmethod
    def get_all_accounts():
        # Exclude the current user if owner or admin
        # Plus if current user is an admin, do not reveal owners
        if session["role"] == ADMIN_ROLE_NAME:
            accounts = AppDB.db_session.query(User, UserBusiness, Role) \
                .join(UserBusiness).join(Role).filter(
                UserBusiness.business_id == session.get("business_id"),
                UserBusiness.emp_id != current_user.emp_id,
                UserBusiness.role_id != Role.get_role_id(OWNER_ROLE_NAME)
            ).all()
        else:
            accounts = AppDB.db_session.query(User, UserBusiness, Role) \
                .join(UserBusiness).join(Role).filter(
                UserBusiness.business_id == session.get("business_id"),
                UserBusiness.emp_id != current_user.emp_id,
            ).all()

        print("accounts: %s" % accounts)

        # Modify the list for the template to use
        return [dict(
            id=account[0].emp_id,
            name=account[0].name,
            deactivated=account[1].is_deactivated,
            role=account[2].name
        ) for account in accounts]

    @staticmethod
    def get_all_roles():
        if session["role"] == ADMIN_ROLE_NAME:
            # admin_related_roles
            roles = AppDB.db_session.query(Role).filter(
                Role.id != Role.get_role_id(OWNER_ROLE_NAME)
            ).all()
        else:
            # owner_related_roles
            roles = AppDB.db_session.query(Role).all()

        return [dict(
            id=role.id,
            name=role.name
        ) for role in roles]


class UserRoleAPI(AppView):
    @staticmethod
    @login_required
    @is_admin
    def put():
        role_assignment_request = request.get_json()

        # Ensure request is JSON formatted
        if not role_assignment_request:
            return ManageAccountsAPI.send_response(
                msg="Request not in JSON",
                status=400
            )

        # Ensure all fields exists and have values
        if not UserRoleAPI.validate_role_assignment_request(role_assignment_request):
            return UserRoleAPI.send_response(
                msg="Fill in all details",
                status=400
            )

        for role in role_assignment_request["roles"]:
            try:
                # Confirm existence of the role
                role_name = role["role"].strip().lower()
                role_id = Role.get_role_id(role_name)
                if not role_id:
                    print("No role with that name")
                    continue

                # Confirm that as an admin, you can perform this role change
                if session["role"] == ADMIN_ROLE_NAME and role_name == OWNER_ROLE_NAME:
                    # An admin cannot change the role to owner
                    print("You don't have privilege to change anything about an owner")
                    continue

                # Confirm existence of employee
                emp_id = role["emp_id"]
                user = AppDB.db_session.query(User).filter(
                    User.emp_id == emp_id
                ).first()
                if not user:
                    print("No user by that description")
                    continue

                # User and role exist, go ahead and find the record
                user_business = AppDB.db_session.query(UserBusiness).filter(
                    UserBusiness.emp_id == emp_id,
                    UserBusiness.business_id == session.get("business_id"),
                ).first()

                # Confirm that an admin is not altering an owner
                if session["role"] == ADMIN_ROLE_NAME and user_business.role_id == Role.get_role_id(OWNER_ROLE_NAME):
                    print("You cannot alter an owner's details")
                    continue

                if not user_business:
                    print("That user does not work for you")
                    continue

                # Prevent owner from deactivating or demoting himself
                if current_user.emp_id == user_business.emp_id and \
                        user_business.role_id == Role.get_role_id(OWNER_ROLE_NAME):
                    print("Cannot demote or deactivate yourself(%s, %s | Owner of(%s))" % (
                        current_user.name,
                        current_user.email,
                        session["business_name"]
                    ))
                    continue

                # Change the user's role in the business
                user_business.role_id = role_id

                # Update user's deactivation status
                user_business.is_deactivated = role["deactivated"]

                AppDB.db_session.commit()
            except SQLAlchemyError as e:
                AppDB.db_session.rollback()
                current_app.logger.error(e)
                current_app.sentry.captureException()

        return ManageAccountsAPI.send_response(
            msg=dict(
                accounts=ManageAccountsAPI.get_all_accounts(),
                roles=ManageAccountsAPI.get_all_roles()
            ),
            status=200
        )

    @staticmethod
    @login_required
    @is_admin
    def post():
        role_addition_request = request.get_json()

        # Ensure request is JSON formatted
        if not role_addition_request:
            return ManageAccountsAPI.send_response(
                msg="Request not in JSON",
                status=400
            )

        # Ensure all fields exists and have values
        if not UserRoleAPI.validate_role_addition_request(role_addition_request):
            return UserRoleAPI.send_response(
                msg="Fill in all details",
                status=400
            )
        try:
            # Confirm existence of the role
            role_name = role_addition_request["role"].strip().lower()
            role_id = Role.get_role_id(role_name)
            if not role_id:
                return UserRoleAPI.send_response(
                    msg="No role with that name",
                    status=404
                )

            # Confirm that as an admin, you can perform this role change
            if session["role"] == ADMIN_ROLE_NAME and role_name == OWNER_ROLE_NAME:
                # An admin cannot change the role to owner
                return UserRoleAPI.send_response(
                    msg="You don't have permission to do this",
                    status=400
                )

            # Confirm existence of email
            email_address = role_addition_request["email"].strip().lower()
            user = AppDB.db_session.query(User).filter(
                User.email == email_address
            ).first()
            if not user:
                return UserRoleAPI.send_response(
                    msg="No user by that email",
                    status=404
                )

            # Confirm role hasn't already been assigned
            user_business = AppDB.db_session.query(UserBusiness).filter(
                UserBusiness.emp_id == user.emp_id,
                UserBusiness.business_id == session.get("business_id"),
            ).first()

            if user_business:
                return UserRoleAPI.send_response(
                    msg="User by that email already assigned a role in the business",
                    status=400
                )

            # Add the user's role in the business
            # First get the current business
            business = AppDB.db_session.query(Business).get(
                session.get("business_id")
            )

            # Then go ahead and create the user's role in the business
            user_business = UserBusiness(
                role_id=role_id
            )
            user_business.business = business
            user_business.user = user
            AppDB.db_session.add(user_business)
            AppDB.db_session.commit()

            return ManageAccountsAPI.send_response(
                msg=dict(
                        accounts=ManageAccountsAPI.get_all_accounts(),
                        roles=ManageAccountsAPI.get_all_roles()
                    ),
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return ManageAccountsAPI.error_in_processing_request()

    @staticmethod
    def validate_role_assignment_request(role_assignment_request):
        if "roles" in role_assignment_request:
            for role in role_assignment_request["roles"]:
                # Key existence check
                if "emp_id" not in role or "role" not in role or "deactivated" not in role:
                    return False
                # Value existence check
                if role["emp_id"] in ["", None] or role["role"] in ["", None] or role["deactivated"] in ["", None]:
                    return False
            return True
        return False

    @staticmethod
    def validate_role_addition_request(role_assignment_request):
        if "role" in role_assignment_request and \
                "email" in role_assignment_request and \
                role_assignment_request["role"] not in ["", None] and \
                role_assignment_request["email"] not in ["", None]:
                return True
        return False


# Create account management view
manage_accounts_view = ManageAccountsAPI.as_view("manage_accounts")
user_role_view = UserRoleAPI.as_view("user_role")

# Create account management blueprint
manage_accounts_bp = Blueprint(
    name="manage_accounts_bp",
    import_name=__name__,
    url_prefix="/manage_accounts",
    static_folder="static",
    template_folder="templates"
)

# Create URL endpoint
manage_accounts_bp.add_url_rule(rule="", view_func=manage_accounts_view)
manage_accounts_bp.add_url_rule(rule="/role", view_func=user_role_view)
