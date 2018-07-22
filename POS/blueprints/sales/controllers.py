import datetime

from flask import Blueprint, render_template, request, current_app, session
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from POS.blueprints.base.app_view import AppView
from POS.models.sales.line_item import LineItem
from POS.models.sales.sales_transaction import SalesTransaction
from POS.models.stock_management.product import Product
from POS.models.user_management.business import Business
from POS.utils import is_cashier, selected_business


class CheckoutAPI(AppView):
    @staticmethod
    @is_cashier
    @selected_business
    def get():
        return render_template(
            template_name_or_list="checkout.html"
        )


class SalesAPI(AppView):
    @staticmethod
    @is_cashier
    @selected_business
    def get():
        pass

    @staticmethod
    @is_cashier
    @selected_business
    def post():
        new_sales_request = request.get_json(silent=True)

        # Ensure request is structured properly
        if not new_sales_request:
            return SalesAPI.send_response(
                msg="Problem with structure of new products request",
                status=400
            )

        if not SalesAPI.validate_new_product_request(new_sales_request):
            return SalesAPI.send_response(
                msg="Missing fields or missing values",
                status=400
            )

        try:
            if len(new_sales_request["line_items"]) > 0:
                from POS import AppDB
                # Get info
                amount_given = new_sales_request["transaction"]["amount_given"]
                current_time = datetime.datetime.now()

                # Model sales transaction
                sales_transaction = SalesTransaction(timestamp=current_time, amount_given=amount_given)

                sales_transaction.business = AppDB.db_session.query(Business).get(session["business_id"])
                sales_transaction.user = current_user

                # Add line items to the transaction
                for line_item_request in new_sales_request["line_items"]:
                    # Get the product associated with the line item
                    product = AppDB.db_session.query(Product).get(line_item_request["product_id"])

                    if product:
                        # Model a line item
                        line_item = LineItem(
                            name=line_item_request["name"],
                            quantity=line_item_request["quantity"],
                            price=line_item_request["price"]
                        )
                        line_item.product = product

                        line_item.sales_transaction = sales_transaction

                AppDB.db_session.add(sales_transaction)
                AppDB.db_session.commit()

            return SalesAPI.send_response(
                msg="Still working on it",
                status=200
            )
        except SQLAlchemyError as e:
            from POS import AppDB
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            if "sentry" in current_app.config:
                current_app.sentry.captureException()
            return SalesAPI.error_in_processing_request()

    @staticmethod
    def validate_new_product_request(new_sales_request):
        if "transaction" in new_sales_request and \
                "amount_given" in new_sales_request["transaction"] and \
                new_sales_request["transaction"]["amount_given"] not in ("", None) and \
                "line_items" in new_sales_request:
                    for line_item in new_sales_request["line_items"]:
                        if "name" in line_item and \
                                line_item["name"] not in ("", None) and \
                                "product_id" in line_item and \
                                line_item["product_id"] not in ("", None) and \
                                "price" in line_item and \
                                line_item["price"] not in ("", None) and \
                                "quantity" in line_item and \
                                line_item["quantity"] not in ("", None):
                            pass
                        else: return False
                    return True
        return False


# Create checkout blueprint
checkout_view = CheckoutAPI.as_view("checkout")

checkout_bp = Blueprint(
    name="checkout_bp",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/checkout"
)

checkout_bp.add_url_rule(rule="", view_func=checkout_view, methods=["GET"])


# Create sales blueprint
sales_view = SalesAPI.as_view("sales")

sales_bp = Blueprint(
    name="sales_bp",
    import_name=__name__,
    url_prefix="/sales"
)

sales_bp.add_url_rule(rule="", view_func=sales_view, methods=["GET", "POST"])
