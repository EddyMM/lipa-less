from flask import redirect, Blueprint, render_template
from flask_login import login_required, current_user

from POS.base.app_view import AppView
from POS.models.base_model import AppDB
from POS.models.business import Business
from POS.models.role import Role
from POS.models.user_business import UserBusiness

from POS.constants import APP_NAME


class DashboardAPI(AppView):
    @staticmethod
    @login_required
    def get(business_id=None):
        if not business_id:
            return redirect(
                location="/login"
            )

        # Confirm business exists
        if not Business.exists(business_id=business_id):
            return redirect(
                location="/business"
            )

        # Check if current user is owner of the specified business
        user_role = AppDB.db_session.query(UserBusiness).filter(
            UserBusiness.emp_id == current_user.emp_id,
            UserBusiness.role_id == Role.get_owner_role_id()
        ).first()

        if not user_role:
            # User is not the owner of this business
            return redirect(
                location="/login"
            )
        # User is the owner of this business, go ahead and render the template

        return render_template(
            template_name_or_list="dashboard.html",
            title="%s: %s" % (APP_NAME, "Dashboard"),
            business_id=business_id
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


@dashboard_bp.route("/")
def index():
    return redirect(
        location="/business"
    )


# Create URL endpoint
dashboard_bp.add_url_rule(rule="/<int:business_id>", view_func=dashboard_view)
