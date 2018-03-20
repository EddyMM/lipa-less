from flask import Blueprint, render_template, request, logging, make_response
from flask.views import MethodView

from ...constants import APP_NAME
from ...models.base_model import db_session
from ...models.user import User


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
                if SignUp.user_exists(user_request["email"]):
                    return make_response(
                        "User by that email already exists",
                        409
                    )

                # User info
                name = user_request["name"]
                email = user_request["email"]
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

                return make_response("User created", 200)
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
        return ("name" in client_request.keys() and
                "email" in client_request.keys() and
                "password" in client_request.keys()) and \
               (client_request["name"] not in ["", None]) and \
               (client_request["email"] not in ["", None]) and \
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
