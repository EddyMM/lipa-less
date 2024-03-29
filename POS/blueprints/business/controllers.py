import uuid

from flask import Blueprint, render_template, request, current_app, redirect, url_for, session
from flask_login import login_required, current_user

from sqlalchemy.exc import SQLAlchemyError

from POS import constants
from POS.blueprints.billing.controllers import BillingAPI
from POS.constants import APP_NAME, OWNER_ROLE_NAME, BILLING_INTERVAL_IN_SECONDS

from POS.blueprints.base.app_view import AppView

from POS.models.base_model import AppDB
from POS.models.billing.ewallet import EWallet
from POS.models.user_management.business import Business
from POS.models.user_management.role import Role
from POS.models.user_management.user_business import UserBusiness


class BusinessAPI(AppView):
    @staticmethod
    @login_required
    def get():
        try:
            """
                Gets and returns a page filled with a list of all businesses
                associated with the current user
            :return:
            """
            # Load list of businesses where user is associated with
            # First get the id of owner role
            businesses = AppDB.db_session.query(Business).join(UserBusiness).filter(
                UserBusiness.emp_id == current_user.emp_id,
                UserBusiness.is_deactivated != True
            ).all()

            businesses = [dict(
                name=business.name,
                id=business.id) for business in businesses]

            # noinspection PyUnresolvedReferences
            return render_template(
                template_name_or_list="business.html",
                title="%s: %s" % (APP_NAME, "business"),
                businesses=businesses
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return BusinessAPI.error_in_processing_request()

    @staticmethod
    @login_required
    def post():
        """
            Adds a new business
        :return:
        """

        business_request = request.get_json()

        if not business_request:
            error = "Request mime type for JSON not specified"
            current_app.logger.warning(error)
            return BusinessAPI.send_response(
                msg=error,
                status=400
            )

        if not BusinessAPI.request_is_filled(business_request):
            return BusinessAPI.send_response(
                msg="Fill in all details",
                status=400
            )
        if BusinessAPI.business_exists(business_request["name"]):
            return BusinessAPI.send_response(
                msg="Business by that name exists",
                status=409
            )

        # Business info
        business_name = business_request["name"].strip().lower()
        contact_number = business_request["contact_number"].strip().lower()

        try:
            # Create business data object
            business = Business(
                name=business_name,
                contact_no=contact_number,
            )

            # Assign owner role to user
            # First find the owner role object
            owner_role_id = Role.get_role_id(OWNER_ROLE_NAME)

            # Owner role exists so associate currently logged in user to it
            # but relative to the business
            user_business = UserBusiness(owner_role_id)
            user_business.business = business
            user_business.user = current_user

            # Add business info to database
            AppDB.db_session.add(business)
            # Add user role info to database
            AppDB.db_session.add(user_business)

            # Create an e-wallet for the business
            ewallet = EWallet()
            ewallet.business = business

            AppDB.db_session.commit()

            session["business_id"] = business.id
            session["business_name"] = business.name
            session["role"] = AppDB.db_session.query(Role).get(owner_role_id).name

            # Start billing user
            business_id = session["business_id"]

            if session.get("billing_job_id"):
                current_app.logger.info("Resuming billing for business: %s" % session["business_name"])
                constants.BILLING_SCH.resume_job(session["billing_job_id"])
            else:
                current_app.logger.info("Starting billing job for business: %s" % session["business_name"])
                billing_job_id = uuid.uuid4()
                session["billing_job_id"] = str(billing_job_id)
                current_app.logger.info("Using Job ID of: %s for business: %s" % (
                    session["billing_job_id"], session["business_name"]))

                constants.BILLING_SCH.add_job(
                    lambda: BillingAPI.bill_user(business_id),
                    "interval",
                    seconds=BILLING_INTERVAL_IN_SECONDS,
                    id=str(billing_job_id)
                )

            return BusinessAPI.send_response(
                msg="Business created",
                business_id=business.id,
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return BusinessAPI.error_in_processing_request()

    @staticmethod
    def request_is_filled(client_request):
        """
        Checks to confirm that the necessary fields exist and are filled
        :param client_request: The JSON request
        :return: True if exists and are filled, False otherwise
        """
        return ("name" in client_request.keys() and
                "contact_number" in client_request.keys()) and \
               (client_request["name"] not in ["", None]) and \
               (client_request["contact_number"] not in ["", None])

    @staticmethod
    def business_exists(name):
        """
            Checks if the business already exists
        :param name: Business name
        :return: True if they have an account, False otherwise
        """
        if AppDB.db_session.query(Business).filter(
                Business.name == name.strip().lower()
        ).first():
            return True
        return False


class SelectBusinessAPI(AppView):
    """
        API to handle the user selections of the business they want to log into
    """
    @staticmethod
    @login_required
    def get(business_id=None):
        try:
            # Confirm that business ID was sent
            if business_id is None:
                return SelectBusinessAPI.send_response(
                    msg="No business ID",
                    status=400
                )

            # Confirm business exists
            if not Business.exists(business_id=business_id):
                return redirect(
                    location=url_for("business_bp.business")
                )

            # Check if current user belongs to the specified business
            user_role = AppDB.db_session.query(UserBusiness).filter(
                UserBusiness.emp_id == current_user.emp_id,
                UserBusiness.business_id == business_id
            ).first()

            if not user_role:
                # User is not a member of this business
                return redirect(
                    location=url_for("login_bp.login")
                )

            # Business exists, store it in the session to know which business
            # the user is going to be interacting with
            session["business_id"] = business_id
            session["business_name"] = AppDB.db_session.query(Business).get(business_id).name
            session["role"] = AppDB.db_session.query(Role).get(user_role.role_id).name

            # Check if user is activated
            if user_role.is_deactivated:
                return SelectBusinessAPI.send_response(
                    msg="You are deactivated",
                    status=403
                )

            # Start billing user
            if session.get("billing_job_id"):
                current_app.logger.info("Resuming billing for business: %s" % session["business_name"])
                constants.BILLING_SCH.resume_job(session["billing_job_id"])
            else:
                current_app.logger.info("Starting billing job for business: %s" % session["business_name"])
                billing_job_id = uuid.uuid4()
                session["billing_job_id"] = str(billing_job_id)
                current_app.logger.info("Using Job ID of: %s for business: %s" % (
                    session["billing_job_id"], session["business_name"]))

                constants.BILLING_SCH.add_job(
                    lambda: BillingAPI.bill_user(business_id),
                    "interval",
                    seconds=BILLING_INTERVAL_IN_SECONDS,
                    id=str(billing_job_id)
                )

            # User belongs to this business, go ahead and redirect them to dashboard
            return redirect(
                location=url_for("dashboard_bp.dashboard")
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return BusinessAPI.error_in_processing_request()


# Create business view
business_view = BusinessAPI.as_view("business")
select_business_view = SelectBusinessAPI.as_view("select_business")

# Create business blueprint
business_bp = Blueprint(
    name="business_bp",
    import_name=__name__,
    url_prefix="/business",
    static_folder="static",
    template_folder="templates"
)

# Create endpoints
business_bp.add_url_rule(
    rule="",
    view_func=business_view
)

business_bp.add_url_rule(
    rule="/select/<int:business_id>",
    view_func=select_business_view
)
