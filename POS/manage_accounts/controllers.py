from flask import Blueprint, render_template, request, session
from flask_login import login_required

from POS.base.app_view import AppView
from POS.models.base_model import AppDB
from POS.models.user import User
from POS.models.business import Business
from POS.models.role import Role
from POS.models.user_business import UserBusiness

from POS.constants import APP_NAME
from POS.utils import selected_business, is_owner


class ManageAccountsAPI(AppView):
    @staticmethod
    @login_required
    @selected_business
    @is_owner
    def get():
        # Get a list of all the user accounts in the business
        accounts = AppDB.db_session.query(User, UserBusiness, Role)\
            .join(UserBusiness).join(Role).filter(
            UserBusiness.business_id == session.get("business_id")
        ).all()

        # Modify the list for the template to use
        accounts = [dict(
            name=account[0].name,
            deactivated=account[1].is_deactivated,
            role=account[2].name
        ) for account in accounts]

        # Get a list of all possible roles in the business so
        # that the owner or admin can select from a variety or roles
        roles = [dict(
            id=role.id,
            name=role.name
        ) for role in AppDB.db_session.query(Role).all()]

        print("Accounts: %s" % accounts)
        print("Roles: %s" % roles)

        # noinspection PyUnresolvedReferences
        return render_template(
            template_name_or_list="manage_accounts.html",
            title="%s: %s" % (APP_NAME, "Accounts"),
            accounts=accounts,
            roles=roles
        )


class UserRoleAPI(AppView):
    @staticmethod
    @login_required
    @selected_business
    @is_owner
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
            # Confirm existence of the role
            role_name = role["role"]
            role_id = Role.get_role_id(role_name)
            if not role_id:
                print("No role with that name")
                continue

            # Confirm existence of email
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

            if not user_business:
                print("That user does not work for you")
                continue

            # Change the user's role in the business
            user_business.role_id = role_id
            AppDB.db_session.commit()

        return ManageAccountsAPI.send_response(
            msg="New list of users",
            status=200
        )

    @staticmethod
    @login_required
    @selected_business
    @is_owner
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

        # Confirm existence of the role
        role_name = role_addition_request["role"]
        role_id = Role.get_role_id(role_name)
        if not role_id:
            return UserRoleAPI.send_response(
                msg="No role with that name",
                status=404
            )

        # Confirm existence of email
        email_address = role_addition_request["email"]
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
            msg="New list of users",
            status=200
        )

    @staticmethod
    def validate_role_assignment_request(role_addition_request):
        if "roles" in role_addition_request:
            for role in role_addition_request["roles"]:
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
