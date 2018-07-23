from flask import Blueprint, render_template, make_response, request, current_app, session
from flask_login import login_required
from io import BytesIO


import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from POS.blueprints.base.app_view import AppView
from POS.blueprints.category.controllers import CategoriesAPI
from POS.models.stock_management.category import Category
from POS.models.stock_management.product import Product
from POS.models.user_management.business import Business
from POS.utils import is_admin, business_is_active


class ManageReportsAPI(AppView):
    @staticmethod
    @login_required
    @is_admin
    @business_is_active
    def get():
        # Get full lists of categories
        categories = CategoriesAPI.get_all_categories()

        return render_template(
            template_name_or_list="reports.html",
            categories=categories
        )


class ProductBrandReportAPI(AppView):
    @staticmethod
    @login_required
    @is_admin
    @business_is_active
    def post():
        if not "category" in request.form:
            current_app.logger.warning("Category for product brand report not sent")

        category_id = request.form["category"]
        from POS import AppDB
        products = AppDB.db_session.query(Product).join(Category).join(Business).filter(
            Category.id == category_id,
            Business.id == session["business_id"]
        ).all()

        """query database for same product but different brands, data_requirements: product name and quantity"""

        product_name = AppDB.db_session.query(Category).get(category_id).name  # this part is fetched from db where name or from UI when user chooses product to query
        product_brand_name = [product.name for product in products]
        product_brand_quantity = [product.quantity for product in products]

        # draw the bar graph to make comparision, this should simply tell the user the quantity of the products in-stock
        fig = Figure()
        ax = fig.add_subplot(111)

        x_pos = np.arange(len(product_brand_name))
        ax.set_xticks(x_pos)
        ax.set_xticklabels(product_brand_name)

        # ax.title(product_name + 'BRANDS IN STOCK')
        ax.set_xlabel('BRAND NAME')
        ax.set_ylabel('QUANTITY IN STOCK')

        ax.bar(x_pos, product_brand_quantity, label=product_name)
        # plt.bar(x_pos, product_brand_quantity, label=product_name)
        ax.legend()

        # save file to pdf
        # plt.savefig('/home/jeffkim/Desktop/projects/applications/python_projects/report_generation/reports/report_two'
        #             '/static/images/product_brand_in_stock.pdf', bbox_inches='tight', pad_inches=1, transparent=True)

        # render image to web page
        canvas = FigureCanvas(fig)
        png_output = BytesIO()
        canvas.print_png(png_output)
        response = make_response(png_output.getvalue())
        response.headers['Content-Type'] = 'image/png'
        return response


class ReorderLevelReportAPI(AppView):
    @staticmethod
    @login_required
    @is_admin
    @business_is_active
    def post():
        if not "category" in request.form:
            current_app.logger.warning("Category for product brand report not sent")

        category_id = request.form["category"]
        from POS import AppDB
        products = AppDB.db_session.query(Product).join(Category).join(Business).filter(
            Category.id == category_id,
            Business.id == session["business_id"]
        ).all()

        """query database for same product but different brands, data_requirements: product name and quantity"""

        product_name = AppDB.db_session.query(Category).get(category_id).name  # this part is fetched from db where name or from UI when user chooses product to query
        product_brand_name = [product.name for product in products]
        product_brand_quantity = [product.quantity for product in products]
        product_brand_re_order = [product.reorder_level for product in products]

        # draw the bar graph to make comparision, this should simply tell the user the quantity of the products in-stock
        fig = Figure()
        ax = fig.add_subplot(111)

        x_pos = np.arange(len(product_brand_name))
        ax.set_xticks(x_pos)
        ax.set_xticklabels(product_brand_name)

        # ax.title(product_name + 'BRANDS IN STOCK')
        ax.set_xlabel('BRAND NAME')
        ax.set_ylabel('QUANTITY IN STOCK')

        # plotting for quantity
        ax.bar(x_pos - 0.2, product_brand_quantity, width=0.4, label='CURRENT QUANTITY')


        # plotting for re-order
        ax.bar(x_pos + 0.2, product_brand_re_order, width=0.4, label='RE-ORDER LEVEL')


        ax.legend()

        # save file to pdf
        # plt.savefig('/home/jeffkim/Desktop/projects/applications/python_projects/report_generation/reports/report_two'
        #             '/static/images/product_brand_in_stock.pdf', bbox_inches='tight', pad_inches=1, transparent=True)

        # render image to web page
        canvas = FigureCanvas(fig)
        png_output = BytesIO()
        canvas.print_png(png_output)
        response = make_response(png_output.getvalue())
        response.headers['Content-Type'] = 'image/png'
        return response


manage_reports_view = ManageReportsAPI.as_view("manage_reports")
product_brand_report_view = ProductBrandReportAPI.as_view("product_brand_report")
reorder_level_report_view = ReorderLevelReportAPI.as_view("reorder_level_report_view")

manage_reports_bp = Blueprint(
    name="manage_reports_bp",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/reports"
)

manage_reports_bp.add_url_rule(rule="", view_func=manage_reports_view)
manage_reports_bp.add_url_rule(rule="/product_brand", view_func=product_brand_report_view)
manage_reports_bp.add_url_rule(rule="/product_brand_reorder_level",
                               view_func=reorder_level_report_view)
