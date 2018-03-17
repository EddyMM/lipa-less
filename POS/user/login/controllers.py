from flask.views import MethodView
from flask import Blueprint, render_template

from ...constants import APP_NAME


class Login(MethodView):
    @staticmethod
    def get():
        # noinspection PyUnresolvedReferences
        return render_template(
            template_name_or_list="login.html",
            title="%s: Login" % APP_NAME
        )


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
login_bp.add_url_rule(rule="/", view_func=login_view)
