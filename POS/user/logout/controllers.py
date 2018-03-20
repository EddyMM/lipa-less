from flask import Blueprint, make_response
from flask.views import MethodView
from flask_login import logout_user


class LogoutAPI(MethodView):
    @staticmethod
    def get():
        logout_user()
        return make_response(
            "Logged out",
            200
        )


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
