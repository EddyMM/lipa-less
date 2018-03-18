from flask import Blueprint, render_template, request, logging, make_response
from flask.views import MethodView

from ...constants import APP_NAME
from ...models.base_model import db_session


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
                return "All is well"
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
        return (
                "business_name" and
                "contact_number" and
                "owner_name" and
                "owner_email" and
                "owner_password" in client_request.keys()) and \
               (client_request["business_name"] not in ["", None]) and \
               (client_request["contact_number"] not in ["", None]) and \
               (client_request["owner_name"] not in ["", None]) and \
               (client_request["owner_email"] not in ["", None]) and \
               (client_request["owner_password"] not in ["", None])


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
