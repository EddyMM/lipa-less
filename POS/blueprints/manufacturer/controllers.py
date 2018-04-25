from flask import Blueprint, request, current_app
from flask_login import login_required

from sqlalchemy.exc import SQLAlchemyError

from POS.blueprints.base.app_view import AppView

from POS.models.stock_management.manufacturer import Manufacturer
from POS.models.base_model import AppDB

from POS.utils import is_admin


class ManufacturerAPI(AppView):
    @staticmethod
    @login_required
    def get():
        try:
            # Get list of all manufacturers
            manufacturers = ManufacturerAPI.get_all_manufacturers()

            return ManufacturerAPI.send_response(
                msg=manufacturers,
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return ManufacturerAPI.error_in_processing_request()

    @staticmethod
    @login_required
    @is_admin
    def post():
        manufacturer_addition_request = request.get_json(silent=True)

        # Check if request has error
        if not manufacturer_addition_request:
            return ManufacturerAPI.error_in_request_response()

        # Validate the request body
        if not ManufacturerAPI.validate_manufacturer_addition_request(manufacturer_addition_request):
            return ManufacturerAPI.validation_error_response()

        # Extract info
        name = manufacturer_addition_request["name"].strip().lower()

        try:
            # Add manufacturer
            manufacturer = Manufacturer(name=name)

            AppDB.db_session.add(manufacturer)
            AppDB.db_session.commit()

            # Get updated list of manufacturers
            manufacturers = ManufacturerAPI.get_all_manufacturers()

            return ManufacturerAPI.send_response(
                msg=manufacturers,
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return ManufacturerAPI.error_in_processing_request()

    @staticmethod
    @login_required
    @is_admin
    def put():
        manufacturer_edit_request = request.get_json(silent=True)

        # Check if request has error
        if not manufacturer_edit_request:
            return ManufacturerAPI.error_in_request_response()

        # Validate the request body
        if not ManufacturerAPI.validate_manufacturer_edit_request(manufacturer_edit_request):
            return ManufacturerAPI.validation_error_response()

        # Extract info
        manufacturer_id = manufacturer_edit_request["id"]
        new_name = manufacturer_edit_request["name"].strip().lower()

        try:
            # Get manufacturer
            manufacturer = AppDB.db_session.query(Manufacturer).filter(
                Manufacturer.id == manufacturer_id
            ).first()

            if not manufacturer:
                return ManufacturerAPI.manufacturer_not_found_response()

            # Edit manufacturer
            manufacturer.name = new_name

            AppDB.db_session.commit()

            # Get updated list of manufacturers
            manufacturers = ManufacturerAPI.get_all_manufacturers()

            return ManufacturerAPI.send_response(
                msg=manufacturers,
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return ManufacturerAPI.error_in_processing_request()

    @staticmethod
    @login_required
    @is_admin
    def delete():
        manufacturer_delete_request = request.get_json(silent=True)

        # Check if request has error
        if not manufacturer_delete_request:
            return ManufacturerAPI.error_in_request_response()

        # Validate the request body
        if not ManufacturerAPI.validate_manufacturer_delete_request(manufacturer_delete_request):
            return ManufacturerAPI.validation_error_response()

        # Extract info
        manufacturer_id = manufacturer_delete_request["id"]

        try:
            # Get manufacturer
            manufacturer = AppDB.db_session.query(Manufacturer).filter(
                Manufacturer.id == manufacturer_id
            ).first()

            if not manufacturer:
                return ManufacturerAPI.manufacturer_not_found_response()

            # Delete manufacturer
            AppDB.db_session.delete(manufacturer)
            AppDB.db_session.commit()

            # Get updated list of manufacturers
            manufacturers = ManufacturerAPI.get_all_manufacturers()

            return ManufacturerAPI.send_response(
                msg=manufacturers,
                status=200
            )
        except SQLAlchemyError as e:
            AppDB.db_session.rollback()
            current_app.logger.error(e)
            current_app.sentry.captureException()
            return ManufacturerAPI.error_in_processing_request()

    @staticmethod
    def validate_manufacturer_addition_request(manufacturer_addition_request):
        if "name" in manufacturer_addition_request and \
                manufacturer_addition_request["name"] not in ("", None):
            return True
        return False

    @staticmethod
    def validate_manufacturer_edit_request(manufacturer_edit_request):
        if "id" in manufacturer_edit_request and \
                "name" in manufacturer_edit_request and \
                manufacturer_edit_request["id"] not in ("", None) and \
                manufacturer_edit_request["name"] not in ("", None):
            return True
        return False

    @staticmethod
    def validate_manufacturer_delete_request(manufacturer_delete_request):
        if "id" in manufacturer_delete_request and \
                manufacturer_delete_request["id"] not in ("", None):
            return True
        return False

    @staticmethod
    def get_all_manufacturers():
        return [dict(
            name=manufacturer.name
        ) for manufacturer in AppDB.db_session.query(Manufacturer).all()]

    @staticmethod
    def manufacturer_not_found_response():
        return ManufacturerAPI.send_response(
            msg="No manufacturer by that description",
            status=404
        )


# Create manufacturer view
manufacturer_view = ManufacturerAPI.as_view(name="manufacturer")

# Create manufacturer blueprint
manufacturer_bp = Blueprint(
    name="manufacturer_bp",
    import_name=__name__,
    url_prefix="/manufacturer"
)

# Create URL endpoints
manufacturer_bp.add_url_rule(rule="", view_func=manufacturer_view)
