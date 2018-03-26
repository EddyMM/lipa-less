from flask import Blueprint, render_template, session
from flask_login import login_required

from POS.base.app_view import AppView

from POS.utils import selected_business
from POS.constants import APP_NAME


class DashboardAPI(AppView):
    @staticmethod
    @login_required
    @selected_business
    def get():
        return render_template(
            template_name_or_list="dashboard.html",
            title="%s: %s" % (APP_NAME, "Dashboard"),
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
