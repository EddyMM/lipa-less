from flask.views import MethodView
from flask import Blueprint, render_template, request, make_response, logging
from flask_login import login_user

from ...constants import APP_NAME
from ...models.base_model import db_session
from ...models.user import User


class Login(MethodView):
    @staticmethod
    def get():
        # noinspection PyUnresolvedReferences
        return render_template(
            template_name_or_list="login.html",
            title="%s: Login" % APP_NAME
        )

    @staticmethod
    def post():
        """
            Validate user identity
        :return:
        """
        user_request = request.get_json()

        if not user_request:
            error = "Request mime type for JSON not specified"
            logging.getLogger().log(
                logging.ERROR,
                error
            )
            return make_response(
                error,
                404
            )

        if not Login.request_is_filled(user_request):
            return make_response(
                "Fill in all details",
                404
            )

        # User info
        email = user_request["email"]
        password = user_request["password"]

        # Find user by that email
        # TODO: handle user login
        user = db_session.query(User).filter(
            User.email == email
        ).first()

        if not user:
            return make_response(
                "User by that email not found",
                404
            )

        # User exists, so confirm password
        if user.confirm_password(password):
            # Register user with login manager
            login_user(user)

            return make_response(
                "Successful login",
                200
            )
        else:
            return make_response(
                "Wrong password",
                403
            )

    @staticmethod
    def request_is_filled(client_request):
        """
        Checks to confirm that the necessary fields exist and are filled
        :param client_request: The JSON request
        :return: True if exists and are filled, False otherwise
        """
        return ("email" in client_request.keys() and
                "password" in client_request.keys()) and \
               (client_request["email"] not in ["", None]) and \
               (client_request["password"] not in ["", None])


# Create login view
login_view = Login.as_view("login")

# Create login blueprint
login_bp = Blueprint(
    name="login_bp",
    import_name=__name__,
    url_prefix="/login",
    template_folder="templates"
)

# Attach URL endpoints
login_bp.add_url_rule(rule="", view_func=login_view)
