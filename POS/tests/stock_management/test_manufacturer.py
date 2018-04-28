from POS.tests.base.base_test_case import BaseTestCase

from POS.models.base_model import AppDB
from POS.models.stock_management.manufacturer import Manufacturer


class TestManufacturer(BaseTestCase):
    def setUp(self):
        self.init_test_app()
        self.create_users()

    def test_get_manufacturers(self):
        # Login as cashier
        self.login_as_cashier()

        # Get list of manufacturers
        rv = self.test_app.get("/manufacturers")

        if rv.headers:
            print("rv.headers: %s, rv.status: %s" % (rv.headers, rv.status))

        # Check if it succeeded
        self.assertIn("200", rv.status)

    def test_manufacturer_addition(self):
        # Login as admin
        self.login_as_admin()

        # Add a manufacturer
        self.add_manufacturer()

        # Confirm that manufacturer was added
        self.assertEqual(AppDB.db_session.query(Manufacturer).count(), 1)

    def test_manufacturer_modification(self):
        # Login as admin
        self.login_as_admin()

        # Add a manufacturer
        self.add_manufacturer()

        # Get the manufacturer
        manufacturer = AppDB.db_session.query(Manufacturer).first()

        # Edit details
        new_name = self.manufacturer_name + "more stuff"
        self.send_json_put(
            endpoint="/manufacturers/{0}".format(manufacturer.id),
            name=new_name
        )

        # Check if details have been modified
        manufacturer = AppDB.db_session.query(Manufacturer).first()

        self.assertEqual(new_name, manufacturer.name)

    def test_manufacturer_deletion(self):
        # Login as admin
        self.login_as_admin()

        # Add a manufacturer
        self.add_manufacturer()

        # Get the manufacturer
        manufacturer = AppDB.db_session.query(Manufacturer).first()

        # Delete manufacturer
        self.send_json_delete(
            endpoint="/manufacturers/{0}".format(manufacturer.id)
        )

        # Confirm manufacturer was removed
        self.assertEqual(AppDB.db_session.query(Manufacturer).count(), 0)

    def add_manufacturer(self):
        self.manufacturer_name = "test_manufacturer"

        self.send_json_post(
            endpoint="/manufacturer",
            name=self.manufacturer_name
        )
