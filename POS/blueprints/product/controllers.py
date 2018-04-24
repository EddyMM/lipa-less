from flask import Blueprint, request, session, current_app
from flask_login import login_required

from sqlalchemy.exc import SQLAlchemyError

from POS.blueprints.base.app_view import AppView

from POS.models.base_model import AppDB
from POS.models.stock_management.product import Product
from POS.models.stock_management.supplier import Supplier
from POS.models.stock_management.manufacturer import Manufacturer
from POS.models.stock_management.category import Category
from POS.models.user_management.business import Business

from POS.utils import is_cashier, is_admin


class ProductAPI(AppView):
    @staticmethod
    @login_required
    @is_cashier
    def get():
        try:
            # Get all products within business
            products = ProductAPI.get_all_products()

            return ProductAPI.send_response(
                msg=products,
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return ProductAPI.error_in_processing_request()

    @staticmethod
    @login_required
    @is_admin
    def post():
        new_products_request = request.get_json(silent=True)

        # Ensure request is structured properly
        if not new_products_request:
            return ProductAPI.send_response(
                msg="Problem with structure of new products request",
                status=400
            )

        if not ProductAPI.validate_new_product_request(new_products_request):
            return ProductAPI.send_response(
                msg="Missing fields or missing values",
                status=400
            )

        # Get info
        name = new_products_request["name"]
        buying_price = new_products_request["buying_price"]
        selling_price = new_products_request["selling_price"]
        quantity = new_products_request["quantity"]
        reorder_level = new_products_request.get("reorder_level", 0)
        description = new_products_request.get("description", None)
        expiration_date = new_products_request.get("expiration_date", None)
        category_id = new_products_request.get("category_id", None)
        supplier_id = new_products_request.get("supplier_id", None)
        manufacturer_id = new_products_request.get("manufacturer_id", None)


        try:
            # Create product
            product = Product(
                name=name,
                buying_price=buying_price,
                selling_price=selling_price,
                quantity=quantity,
                description=description,
                expiration_date=expiration_date,
                reorder_level=reorder_level
            )

            # Relationships
            if supplier_id:
                product.supplier = AppDB.db_session.query(Supplier).get(supplier_id)
            if manufacturer_id:
                product.manufacturer = AppDB.db_session.query(Manufacturer).get(manufacturer_id)
            if category_id:
                product.category = AppDB.db_session.query(Category).get(category_id)

            product.business = AppDB.db_session.query(Business).get(session["business_id"])

            AppDB.db_session.add(product)
            AppDB.db_session.commit()

            # Get updated list of products
            products = ProductAPI.get_all_products()

            return ProductAPI.send_response(
                msg=products,
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return ProductAPI.error_in_processing_request()

    @staticmethod
    @login_required
    @is_admin
    def put():
        modify_products_request = request.get_json(silent=True)

        # Ensure request is structured properly
        if not modify_products_request:
            return ProductAPI.send_response(
                msg="Problem with structure of new products request",
                status=400
            )

        if not ProductAPI.validate_modify_product_request(modify_products_request):
            return ProductAPI.send_response(
                msg="Missing fields or missing values",
                status=400
            )

        # Get info
        product_id = modify_products_request["id"]
        name = modify_products_request["name"]
        buying_price = modify_products_request["buying_price"]
        selling_price = modify_products_request["selling_price"]
        quantity = modify_products_request["quantity"]
        reorder_level = modify_products_request.get("reorder_level", 0)
        description = modify_products_request.get("description", None)
        expiration_date = modify_products_request.get("expiration_date", None)
        category_id = modify_products_request.get("category_id", None)
        supplier_id = modify_products_request.get("supplier_id", None)
        manufacturer_id = modify_products_request.get("manufacturer_id", None)

        try:
            # Get product
            product = AppDB.db_session.query(Product).get(product_id)

            if not product:
                return ProductAPI.send_response(
                    msg="No product by that description",
                    status=404
                )

            product.name = name,
            product.buying_price = buying_price,
            product.selling_price = selling_price,
            product.quantity = quantity,
            product.description = description,
            product.expiration_date = expiration_date,
            product.reorder_level = reorder_level

            # Relationships
            if supplier_id:
                product.supplier = AppDB.db_session.query(Supplier).get(supplier_id)
            if manufacturer_id:
                product.manufacturer = AppDB.db_session.query(Manufacturer).get(manufacturer_id)
            if category_id:
                product.category = AppDB.db_session.query(Category).get(category_id)

            product.business = AppDB.db_session.query(Business).get(session["business_id"])

            AppDB.db_session.commit()

            # Get updated list of products
            products = ProductAPI.get_all_products()

            return ProductAPI.send_response(
                msg=products,
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return ProductAPI.error_in_processing_request()

    @staticmethod
    @login_required
    @is_admin
    def delete():
        delete_product_request = request.get_json(silent=True)

        # Ensure request is structured properly
        if not delete_product_request:
            return ProductAPI.send_response(
                msg="Problem with structure of new products request",
                status=400
            )

        if not ProductAPI.validate_delete_product_request(delete_product_request):
            return ProductAPI.send_response(
                msg="Missing fields or missing values",
                status=400
            )

        # Get info
        product_id = delete_product_request["id"]

        try:
            # Get product
            product = AppDB.db_session.query(Product).get(product_id)

            if not product:
                return ProductAPI.send_response(
                    msg="No product by that description",
                    status=404
                )

            AppDB.db_session.delete(product)
            AppDB.db_session.commit()

            # Get updated list of products
            products = ProductAPI.get_all_products()

            return ProductAPI.send_response(
                msg=products,
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return ProductAPI.error_in_processing_request()

    @staticmethod
    def validate_new_product_request(new_product_request):
        if "name" in new_product_request and \
                "buying_price" in new_product_request and \
                "selling_price" in new_product_request and \
                "quantity" in new_product_request and \
                new_product_request["name"] not in ("", None) and \
                new_product_request["buying_price"] not in ("", None) and \
                new_product_request["selling_price"] not in ("", None) and \
                new_product_request["quantity"] not in ("", None):
            return True
        return False

    @staticmethod
    def validate_modify_product_request(modify_product_request):
        if "id" in modify_product_request and \
                "name" in modify_product_request and \
                "buying_price" in modify_product_request and \
                "selling_price" in modify_product_request and \
                "quantity" in modify_product_request and \
                modify_product_request["id"] not in ("", None) and \
                modify_product_request["name"] not in ("", None) and \
                modify_product_request["buying_price"] not in ("", None) and \
                modify_product_request["selling_price"] not in ("", None) and \
                modify_product_request["quantity"] not in ("", None):
            return True
        return False

    @staticmethod
    def validate_delete_product_request(delete_product_request):
        if "id" in delete_product_request and \
                delete_product_request["id"] not in ("", None):
            return True
        return False

    @staticmethod
    def get_all_products():
        products = [dict(
            id=product.id,
            name=product.name,
            buying_price=product.buying_price,
            selling_price=product.selling_price,
            description=product.description
        ) for product in AppDB.db_session.query(Product).filter(
            Product.business_id == session["business_id"]
        ).all()]

        return products


# Create view
product_view = ProductAPI.as_view("product")

# Create blueprint
product_bp = Blueprint(
    name="product_bp",
    import_name=__name__,
    url_prefix="/product"
)

# Create URL endpoints
product_bp.add_url_rule(rule="", view_func=product_view)
