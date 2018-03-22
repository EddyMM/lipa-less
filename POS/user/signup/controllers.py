from flask import Blueprint, render_template, request, redirect, url_for, logging
from flask_login import login_user

from ...base.app_view import AppView
from ...constants import APP_NAME
from ...models.base_model import AppDB
from ...models.user import User


class SignUp(AppView):
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
                    return SignUp.send_response(
                        msg="User by that email already exists",
                        status=409
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
                AppDB.db_session.add(user)
                AppDB.db_session.commit()

                # Log event
                logger = logging.getLogger()
                logger.setLevel(logging.DEBUG)
                logger.log(
                    logging.DEBUG,
                    "User(%s), Email(%s) created" % (
                        user.name,
                        user.email
                    )
                )

                # log the user in
                login_user(user)

                return SignUp.send_response(
                    msg="User created",
                    status=200
                )
            else:
                return SignUp.send_response(
                    msg="Fill in all details",
                    status=400
                )
        else:
            error = "Request mime type for JSON not specified"
            logging.getLogger().log(
                logging.ERROR,
                error
            )
            return SignUp.send_response(
                msg=error,
                status=400
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
        if AppDB.db_session.query(User).filter(
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
