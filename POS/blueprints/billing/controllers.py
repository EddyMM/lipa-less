from flask import request, make_response, Blueprint, current_app
from sqlalchemy.exc import SQLAlchemyError

from POS.models.base_model import AppDB
from POS.blueprints.base.app_view import AppView
from POS.models.billing.billing_transaction import BillingTransaction
from POS.models.billing.ewallet import EWallet


class BillingAPI(AppView):
    @staticmethod
    def post():
        # AT payments callback contacted
        billing_request = request.get_json(force=True)

        if not billing_request:
            return BillingAPI.error_in_request_response()

        # Ensure request has all fiends filled
        if not BillingAPI.validate_billing_request(billing_request):
            return BillingAPI.validation_error_response()

        if billing_request:
            print("Payment Request Details of type({1}): ({0}) ".format(len(billing_request), type(billing_request)))
            print("Provider: {0}".format(billing_request["provider"]))
            print("Client Account: {0}".format(billing_request["clientAccount"]))
            print("Product name: {0}".format(billing_request["productName"]))
            print("Value: {0}".format(billing_request["value"]))

            value = float(billing_request["value"][3:])
            client_account = int(billing_request["clientAccount"])

            if not (EWallet.exists(client_account)):
                return make_response("No account by that ID", 400)

            try:
                # Create a new billing transaction
                billing_transaction = BillingTransaction(value)
                # Associate the transaction with the business ewallet
                current_business_ewallet = EWallet.get_ewallet_by_id(client_account)
                current_business_ewallet.billing_transactions.append(billing_transaction)

                # Increment ewallet with amount
                current_business_ewallet.balance += value

                AppDB.db_session.add(billing_transaction)
                AppDB.db_session.commit()
            except SQLAlchemyError as e:
                AppDB.db_session.rollback()
                current_app.logger.error(e)
                current_app.sentry.captureException()
                return BillingAPI.error_in_processing_request()

        return make_response("ATP contacted me", 200)

    @staticmethod
    def validate_billing_request(billing_request: request) -> bool:
        if "provider" in billing_request and \
                "clientAccount" in billing_request and \
                "productName" in billing_request and \
                "value" in billing_request and \
                billing_request["provider"] not in ("", None) and \
                billing_request["clientAccount"] not in ("", None) and \
                billing_request["productName"] not in ("", None) and \
                billing_request["value"] not in ("", None):
            return True
        return False


# Create category blueprint
billing_view = BillingAPI.as_view("billing")

billing_bp = Blueprint(
    name="billing_bp",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/billing"
)

billing_bp.add_url_rule(rule="", view_func=billing_view, methods=["POST"])
