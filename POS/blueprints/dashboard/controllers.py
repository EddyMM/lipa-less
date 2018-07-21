from flask import Blueprint, render_template
from flask_login import login_required

from POS.blueprints.base.app_view import AppView

from POS.utils import selected_business, business_is_active
from POS import constants


class DashboardAPI(AppView):
    @staticmethod
    @login_required
    @selected_business
    @business_is_active
    def get():
        return render_template(
            template_name_or_list="dashboard.html",
            title="%s: %s" % (constants.APP_NAME, "Dashboard"),
        )

    @staticmethod
    @login_required
    def post():
        pass


# Create dashboard view
dashboard_view = DashboardAPI.as_view("dashboard")

# Create dashboard blueprint
dashboard_bp = Blueprint(
    name="dashboard_bp",
    import_name=__name__,
    url_prefix="/dashboard",
    static_folder="static",
    template_folder="templates"
)

# Create URL endpoint
dashboard_bp.add_url_rule(rule="", view_func=dashboard_view)
