from flask import Blueprint, redirect, url_for, session
from flask_login import logout_user

from ...base.app_view import AppView


class LogoutAPI(AppView):
    @staticmethod
    def get():
        logout_user()

        # Clear session info
        session.clear()

        return redirect(url_for("login_bp.login"))


# Create logout view
logout_view = LogoutAPI.as_view("logout")

# Create logout blueprint
logout_bp = Blueprint(
    name="logout_bp",
    import_name=__name__,
    url_prefix="/logout"
)

# Create logout endpoint
logout_bp.add_url_rule(rule="", view_func=logout_view)
