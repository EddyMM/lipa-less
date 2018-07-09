from flask import request, make_response, Blueprint

from POS.blueprints.base.app_view import AppView


class BillingAPI(AppView):
    @staticmethod
    def post():
        "AT payments callback contacted"

        if request.method == "POST":
            req_details = request.get_json(force=True)

            if req_details:
                print("Payment Request Details of type({1}): ({0}) ".format(len(req_details), type(req_details)))
                print("Provider: {0}".format(req_details["provider"]))
                print("Client Account: {0}".format(req_details["clientAccount"]))
                print("Product name: {0}".format(req_details["productName"]))
                print("Value: {0}".format(req_details["value"]))

        return make_response("ATP contacted me", 200)


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
