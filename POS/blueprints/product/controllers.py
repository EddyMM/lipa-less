from flask import Blueprint, request

from POS.blueprints.base.app_view import AppView


class ProductAPI(AppView):
    @staticmethod
    def get():
        return "Get product(s)"

    @staticmethod
    def post():
        new_products_request = request.get_json()

        # Ensure request is structured properly
        if not new_products_request:
            return ProductAPI.send_response(
                msg="Problem with structure of new products request",
                status=400
            )

        if not ProductAPI.validate_new_products_request(new_products_request):
            return ProductAPI.send_response(
                msg="Missing fields or missing values",
                status=400
            )

        return "Add new product(s)"

    @staticmethod
    def put():
        return "Modify product(s)"

    @staticmethod
    def delete():
        return "Delete product(s)"

    @staticmethod
    def validate_new_products_request(new_products_request):
        products = new_products_request["products"]
        if products and \
                products["name"] not in ("", None) and \
                products["buying_price"] not in ("", None) and \
                products["selling_price"] not in ("", None) and \
                products["quantity"] not in ("", None):
            return True
        return False


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
