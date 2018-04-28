from flask import Blueprint, request, session, current_app, render_template
from flask_login import login_required

from sqlalchemy.exc import SQLAlchemyError

from typing import List

from POS.blueprints.base.app_view import AppView

from POS.models.base_model import AppDB
from POS.models.stock_management.category import Category
from POS.models.user_management.business import Business

from POS.utils import is_admin, is_cashier


class CategoryAPI(AppView):
    @staticmethod
    @login_required
    @is_cashier
    def get():
        pass

    @staticmethod
    @login_required
    @is_admin
    def post():
        new_category_request = request.get_json(silent=True)

        if not new_category_request:
            return CategoryAPI.error_in_request_response()

        # Ensure request has all fiends filled
        if not CategoryAPI.validate_new_category_request(new_category_request):
            return CategoryAPI.validation_error_response()

        # Fetch the info
        name = new_category_request["name"].strip().lower()
        description = new_category_request["description"].strip().lower()

        try:
            # Create category instance
            category = Category(name, description)

            # Associate the category with the business
            business = AppDB.db_session.query(Business).get(session["business_id"])
            category.business = business

            # Add and commit instance
            AppDB.db_session.add(category)
            AppDB.db_session.commit()

            # Get full lists of categories
            categories = CategoriesAPI.get_all_categories()

            return CategoriesAPI.send_response(
                msg=dict(categories=categories),
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return CategoriesAPI.error_in_processing_request()

    @staticmethod
    def validate_new_category_request(new_category_request: request) -> bool:
        if "name" in new_category_request and \
                "description" in new_category_request and \
                new_category_request["name"] not in ("", None) and \
                new_category_request["description"] not in ("", None):
            return True
        return False


class CategoriesAPI(AppView):
    @staticmethod
    @login_required
    @is_cashier
    def get():
        try:
            # Get full lists of categories
            categories = CategoriesAPI.get_all_categories()

            return render_template(
                template_name_or_list="categories.html",
                categories=categories
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return CategoriesAPI.error_in_processing_request()

    @staticmethod
    @login_required
    @is_admin
    def put(category_id):
        if not category_id:
            return CategoriesAPI.send_response(
                msg="Category ID not specified",
                status=400
            )

        new_categories_request = request.get_json(silent=True)

        if not new_categories_request:
            return CategoriesAPI.send_response(
                msg="Problem with request type or structure",
                status=400
            )

        # Ensure request has all fields filled
        if not CategoriesAPI.validate_edit_category_request(new_categories_request):
            return CategoriesAPI.send_response(
                msg="Missing fields or values",
                status=400
            )

        name = new_categories_request["name"].strip().lower()
        description = new_categories_request["description"].strip().lower()

        try:
            # Get category
            category = CategoriesAPI.get_category_within_business(category_id)

            if not category:
                return CategoriesAPI.send_response(
                    msg="No category by that description",
                    status=404
                )

            # Edit the fields
            category.name = name
            category.description = description

            # Commit changes
            AppDB.db_session.commit()

            # Get updated list of categories
            categories = CategoriesAPI.get_all_categories()

            return CategoriesAPI.send_response(
                msg=dict(categories=categories),
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return CategoriesAPI.error_in_processing_request()

    @staticmethod
    @login_required
    @is_admin
    def delete(category_id):
        if not category_id:
            return CategoriesAPI.send_response(
                msg="Category ID not specified",
                status=400
            )

        try:
            # Get the category to delete
            category = CategoriesAPI.get_category_within_business(category_id)

            if not category:
                return CategoriesAPI.send_response(
                    msg="No category by that description",
                    status=404
                )

            # Delete the category
            AppDB.db_session.delete(category)
            AppDB.db_session.commit()

            # Get updated list of categories
            categories = CategoriesAPI.get_all_categories()

            return CategoriesAPI.send_response(
                msg=dict(categories=categories),
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return CategoriesAPI.error_in_processing_request()

    @staticmethod
    def validate_edit_category_request(edit_category_request: request) -> bool:
        if "name" in edit_category_request and \
                "description" in edit_category_request and \
                edit_category_request["name"] not in ("", None) and \
                edit_category_request["description"] not in ("", None):
            return True
        return False

    @staticmethod
    def get_all_categories() -> List[dict]:
        categories = [dict(
            num=num+1,
            id=category.id,
            name=category.name,
            description=category.description
        ) for num, category in enumerate(AppDB.db_session.query(Category).filter(
                Category.business_id == session["business_id"]
        ).all())]

        return categories

    @staticmethod
    def get_category_within_business(category_id: int) -> Category:
        return AppDB.db_session.query(Category).filter(
            Category.id == category_id,
            Category.business_id == session["business_id"]
        ).first()


# Create categories blueprint
categories_view = CategoriesAPI.as_view("categories")

categories_bp = Blueprint(
    name="categories_bp",
    import_name=__name__,
    template_folder="templates",
    url_prefix="/categories"
)

categories_bp.add_url_rule(rule="", view_func=categories_view, methods=["GET"])
categories_bp.add_url_rule(rule="/<int:category_id>", view_func=categories_view, methods=["PUT", "DELETE"])

# Create category blueprint
category_view = CategoryAPI.as_view("category")

category_bp = Blueprint(
    name="category_bp",
    import_name=__name__,
    template_folder="templates",
    url_prefix="/category"
)

category_bp.add_url_rule(rule="", view_func=category_view, methods=["GET", "POST"])
