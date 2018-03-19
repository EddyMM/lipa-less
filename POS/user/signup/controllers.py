from flask import Blueprint, render_template, request, logging, make_response
from flask.views import MethodView

from ...constants import APP_NAME, OWNER_ROLE_NAME
from ...models.base_model import db_session
from ...models.user import User
from ...models.business import Business
from ...models.role import Role
from ...models.user_role import UserRole


class SignUp(MethodView):
    @staticmethod
    def get():
        # noinspection PyUnresolvedReferences
        return render_template("signup.html", title="%s: %s" % (APP_NAME, "Signup"))

    @staticmethod
    def post():
        user_request = request.get_json()

        if user_request:
            if SignUp.request_is_filled(user_request):
                if SignUp.user_exists(user_request["owner_email"]):
                    return make_response(
                        "User by that email already exists",
                        409
                    )

                # Business info
                business_name = user_request["business_name"]
                contact_number = user_request["contact_number"]

                # Owner info
                name = user_request["owner_name"]
                email = user_request["owner_email"]
                password = user_request["password"]

                # Create user data object
                user = User(
                    name=name,
                    email=email,
                    password=password
                )

                # Add user to the database
                db_session.add(user)
                db_session.commit()

                # Create business data object
                business = Business(
                    name=business_name,
                    contact_no=contact_number,
                    emp_id=user.emp_id
                )

                # Add business info to database
                db_session.add(business)
                db_session.commit()

                # Assign an "owner" role to the user
                # First find the owner role object
                owner_role = db_session.query(Role).filter(
                    Role.name == OWNER_ROLE_NAME
                ).first()

                if not owner_role:
                    # Owner role has not been created yet, so log this occurrence
                    # and send a 500 error
                    error_msg = "Problem creating owner account. We are working on it"
                    logging.getLogger().log(
                        logging.ERROR,
                        error_msg
                    )
                    return make_response(
                        error_msg,
                        500
                    )

                # Owner exists so add it to the user-role model
                user_role = UserRole(
                    emp_id=user.emp_id,
                    role_id=owner_role.id
                )

                # Assign role in database
                db_session.add(user_role)
                db_session.commit()

                return make_response("Owner created", 200)
            else:
                return make_response(
                    "Fill in all details",
                    404
                )
        else:
            error = "Request mime type for JSON not specified"
            logging.getLogger().log(
                logging.ERROR,
                error
            )
            return make_response(
                error,
                404
            )

    @staticmethod
    def request_is_filled(client_request):
        """
        Checks to confirm that the necessary fields exist and are filled
        :param client_request: The JSON request
        :return: True if exists and are filled, False otherwise
        """
        return (
                "business_name" and
                "contact_number" and
                "owner_name" and
                "owner_email" and
                "password" in client_request.keys()) and \
               (client_request["business_name"] not in ["", None]) and \
               (client_request["contact_number"] not in ["", None]) and \
               (client_request["owner_name"] not in ["", None]) and \
               (client_request["owner_email"] not in ["", None]) and \
               (client_request["password"] not in ["", None])

    @staticmethod
    def user_exists(email):
        """
            Checks if the user already has an account
        :param email: User email
        :return: True if they have an account, False otherwise
        """
        if db_session.query(User).filter(
            User.email == email
        ).first():
            return True
        return False


# Create signup view
signup_view = SignUp.as_view("signup")

# Create sign up blueprint
signup_bp = Blueprint(
    name="signup_bp",
    import_name=__name__,
    template_folder="templates",
    url_prefix="/signup",
    static_folder="static")

# Assign endpoint URLs
signup_bp.add_url_rule("", view_func=signup_view)
