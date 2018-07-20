from flask import Blueprint, redirect, url_for, session, current_app
from flask_login import logout_user, current_user

from ...base.app_view import AppView
from POS import constants


class LogoutAPI(AppView):
    @staticmethod
    def get():
        # Stop billing the user
        if current_user.is_authenticated and constants.BILLING_SCH:
            if session.get("billing_job_id") and constants.BILLING_SCH.get_job(session["billing_job_id"]):
                billing_job = constants.BILLING_SCH.get_job(session["billing_job_id"])

                current_app.logger.info("Current jobs: %s" % constants.BILLING_SCH.get_jobs())
                current_app.logger.info("Pausing billing job for business: %s with ID: %s" % (
                   session["business_name"], session["billing_job_id"]))

                constants.BILLING_SCH.pause_job(session["billing_job_id"])
            else:
                current_app.logger.warning("Billing Job: None for business: %s" % session["business_name"])
        else:
            current_app.logger.warning("Billing Schedule(None) for business: %s" % session["business_name"])

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
