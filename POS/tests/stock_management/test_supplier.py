from POS.tests.base.base_test_case import BaseTestCase

from POS.models.base_model import AppDB
from POS.models.stock_management.supplier import Supplier


class TestSupplier(BaseTestCase):
    supplier_name = "test_supplier"
    supplier_contact_person = "test_supplier"
    supplier_contact_number = "0718234567"

    def setUp(self):
        self.init_test_app()
        self.create_users()

    def test_get_all_suppliers(self):
        # Login as cashier
        self.login_as_cashier()

        # Get suppliers
        rv = self.test_app.get("/suppliers")

        self.assertIn("200", rv.status)

    def test_add_supplier(self):
        # Login as admin
        self.login_as_admin()

        # Create a supplier
        self.create_supplier()

        # Check if supplier has been added
        self.assertEqual(AppDB.db_session.query(Supplier).count(), 1)

    def test_modify_supplier(self):
        # Login as admin
        self.login_as_admin()

        # Create supplier
        self.create_supplier()

        # Modify the supplier
        new_supplier_name = self.supplier_name + " more stuff"
        new_supplier_contact_person = self.supplier_contact_person + " more stuff"
        new_supplier_contact_number = self.supplier_contact_number + " more stuff"

        supplier = AppDB.db_session.query(Supplier).first()

        self.send_json_put(
            endpoint="/suppliers/{0}".format(supplier.id),
            name=new_supplier_name,
            contact_person=new_supplier_contact_person,
            contact_number=new_supplier_contact_number
        )

        supplier = AppDB.db_session.query(Supplier).first()

        # Check if changes were made
        self.assertEqual(new_supplier_name, supplier.name)
        self.assertEqual(new_supplier_contact_person, supplier.contact_person)
        self.assertEqual(new_supplier_contact_number, supplier.contact_no)

    def delete_supplier(self):
        # Login as admin
        self.login_as_admin()

        # Create supplier
        self.create_supplier()

        # Delete supplier
        supplier = AppDB.db_session.query(Supplier).first()

        self.send_json_post(
            "/supplier",
            id=supplier.id
        )

        self.assertEqual(AppDB.db_session.query(Supplier).count(), 0)

    def create_supplier(self):
        self.send_json_post(
            endpoint="/supplier",
            name=TestSupplier.supplier_name,
            contact_person=TestSupplier.supplier_contact_person,
            contact_number=TestSupplier.supplier_contact_number
        )
