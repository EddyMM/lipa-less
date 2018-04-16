from flask import Blueprint, request

from POS.blueprints.base.app_view import AppView
from POS.models.base_model import AppDB
from POS.models.stock_management.supplier import Supplier


class SupplierAPI(AppView):
    @staticmethod
    def get():
        suppliers = SupplierAPI.get_all_suppliers()

        return SupplierAPI.send_response(
            msg=suppliers,
            status=200
        )

    @staticmethod
    def post():
        # Capture request
        supplier_addition_request = request.get_json(silent=True)

        if not supplier_addition_request:
            return SupplierAPI.error_in_request_response()

        # Validate the request
        if not SupplierAPI.validate_supplier_addition_request(supplier_addition_request):
            return SupplierAPI.validation_error_response()

        # Get info
        name = supplier_addition_request["name"]
        contact_person = supplier_addition_request["contact_person"]
        contact_number = supplier_addition_request["contact_number"]

        # Model the supplier
        supplier = Supplier(
            name=name,
            contact_person=contact_person,
            contact_no=contact_number
        )

        # Add supplier
        AppDB.db_session.add(supplier)
        AppDB.db_session.commit()

        # Get update list of suppliers
        suppliers = SupplierAPI.get_all_suppliers()

        return SupplierAPI.send_response(
            msg=suppliers,
            status=200
        )

    @staticmethod
    def put():
        # Capture request
        supplier_modification_request = request.get_json(silent=True)

        if not supplier_modification_request:
            return SupplierAPI.error_in_request_response()

        # Validate the request
        if not SupplierAPI.validate_supplier_addition_request(supplier_modification_request):
            return SupplierAPI.validation_error_response()

        # Get info
        supplier_id = supplier_modification_request["id"]
        name = supplier_modification_request["name"]
        contact_person = supplier_modification_request["contact_person"]
        contact_number = supplier_modification_request["contact_number"]

        # Get the supplier
        supplier = AppDB.db_session.query(Supplier).filter(
            Supplier.id == supplier_id
        ).first()

        if not supplier:
            return SupplierAPI.send_response(
                msg="No supplier by that description",
                status=404
            )
        
        supplier.name = name
        supplier.contact_person = contact_person
        supplier.contact_no = contact_number

        # Commit changes
        AppDB.db_session.commit()

        # Get update list of suppliers
        suppliers = SupplierAPI.get_all_suppliers()

        return SupplierAPI.send_response(
            msg=suppliers,
            status=200
        )

    @staticmethod
    def delete():
        # Capture request
        supplier_deletion_request = request.get_json(silent=True)

        if not supplier_deletion_request:
            return SupplierAPI.error_in_request_response()

        # Validate the request
        if not SupplierAPI.validate_supplier_deletion_request(supplier_deletion_request):
            return SupplierAPI.validation_error_response()

        # Get the supplier
        supplier_id = supplier_deletion_request["id"]
        supplier = AppDB.db_session.query(Supplier).get(supplier_id)

        # Check if supplier exists
        if not supplier:
            return SupplierAPI.send_response(
                msg="No supplier by that description",
                status=404
            )

        # Remove supplier
        AppDB.db_session.delete(supplier)
        AppDB.db_session.commit()

        # Get the update list of suppliers
        suppliers = SupplierAPI.get_all_suppliers()

        return SupplierAPI.send_response(
            msg=suppliers,
            status=200
        )

    @staticmethod
    def validate_supplier_addition_request(supplier_addition_request):
        if "name" in supplier_addition_request and \
                "contact_person" in supplier_addition_request and \
                "contact_number" in supplier_addition_request and \
                supplier_addition_request["name"] not in ("", None) and \
                supplier_addition_request["contact_person"] not in ("", None) and \
                supplier_addition_request["contact_number"] not in ("", None):
            return True
        return False

    @staticmethod
    def validate_supplier_modification_request(supplier_modification_request):
        if "id" in supplier_modification_request and \
                "name" in supplier_modification_request and \
                "contact_person" in supplier_modification_request and \
                "contact_number" in supplier_modification_request and \
                supplier_modification_request["id"] not in ("", None) and \
                supplier_modification_request["name"] not in ("", None) and \
                supplier_modification_request["contact_person"] not in ("", None) and \
                supplier_modification_request["contact_number"] not in ("", None):
            return True
        return False

    @staticmethod
    def validate_supplier_deletion_request(supplier_deletion_request):
        if "id" in supplier_deletion_request and \
                supplier_deletion_request["id"] not in ("", None):
            return True
        return False

    @staticmethod
    def get_all_suppliers():
        suppliers = AppDB.db_session.query(Supplier).all()
        return [
            dict(
                name=supplier.name,
                contact_person=supplier.contact_person,
                contact_number=supplier.contact_no
            )for supplier in suppliers
        ]


# Supplier view
supplier_view = SupplierAPI.as_view(name="supplier_bp")

# Supplier blueprint
supplier_bp = Blueprint(
    name="supplier_bp",
    import_name=__name__,
    url_prefix="/supplier"
)

# Supplier URL endpoints
supplier_bp.add_url_rule(rule="", view_func=supplier_view)
