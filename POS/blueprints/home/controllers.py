from flask import render_template, Blueprint
from flask.views import MethodView

from POS.constants import APP_NAME


class Home(MethodView):
    @staticmethod
    def get():
        # noinspection PyUnresolvedReferences
        return render_template("homepage.html", title=APP_NAME)


# Create view
home_view = Home.as_view("home")

# Create a blueprint instance
home_bp = Blueprint("home_bp", __name__, template_folder="templates")

# Specify the URL endpoints
home_bp.add_url_rule("/", view_func=home_view)
