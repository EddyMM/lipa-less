from flask import Blueprint, render_template
from flask.views import MethodView

from ...constants import APP_NAME


class SignUp(MethodView):
    @staticmethod
    def get():
        # noinspection PyUnresolvedReferences
        return render_template("signup.html", title="%s: %s" % (APP_NAME, "Signup"))


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
signup_bp.add_url_rule("/", view_func=signup_view)
