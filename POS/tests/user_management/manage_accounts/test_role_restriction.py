import unittest

from POS.models.base_model import AppDB
from POS.tests.base.base_test_case import BaseTestCase
from POS.utils import is_cashier, is_admin, is_owner

from POS import app


class TestManageAccounts(BaseTestCase):
    def setUp(self):
        TestManageAccounts.confirm_app_in_testing_mode()
        app.testing = True
        app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
        self.test_app = app.test_client()

        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()
        AppDB.BaseModel.metadata.create_all()

        from POS.models.user_management.role import Role
        AppDB.load_default_roles(Role)

        # Create 3 users: owner, admin, cashier
        self.create_users()

    def tearDown(self):
        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()

    def test_cashier_restriction(self):
        """
            Test if cashier decorator function truly restricts
            certain functions or methods from being accessed by someone
            with at least cashier level clearance
        :return:
        """
        # Maintain context throughout
        with self.test_app:
            # Login as cashier
            self.login(
                email=self.cashier_email,
                password=self.cashier_password
            )

            # Select business
            self.select_business(self.business_id)

            def test_func():
                return "test_func"

            wrapper = is_cashier(test_func)

            response = wrapper()

            # Logout as cashier
            self.logout()

        self.assertEqual(response, test_func())

    def test_admin_restriction(self):
        """
            Test if admin decorator function truly restricts
            certain functions or methods from being accessed by someone
            with at least admin level clearance
            :return:
        """
        # Maintain context throughout
        with self.test_app:
            # Login as admin
            self.login(
                email=self.admin_email,
                password=self.admin_password
            )

            # Select business
            self.select_business(self.business_id)

            def test_func():
                return "test_func"

            wrapper = is_admin(test_func)

            print("test_func: %s" % test_func())
            print("is_admin(test_func): %s" % wrapper())

            response = wrapper()

            # Logout as admin
            self.logout()

        self.assertEqual(response, test_func())

        # Go ahead to ensure that cashier cannot run the function
        with self.test_app:
            # Login as cashier
            self.login(
                email=self.cashier_email,
                password=self.cashier_password
            )
            # Select business
            self.select_business(self.business_id)

            def test_func():
                return "test_func"

            wrapper = is_admin(test_func)

            response = wrapper()

            # Logout as cashier
            self.logout()

        self.assertNotEqual(response, test_func())

    def test_owner_restriction(self):
        """
                    Test if admin decorator function truly restricts
                    certain functions or methods from being accessed by someone
                    with at least admin level clearance
                    :return:
                """
        # Maintain context throughout
        with self.test_app:
            # Login as owner
            self.login(
                email=self.owner_email,
                password=self.owner_password
            )

            # Select business
            self.select_business(self.business_id)

            def test_func():
                return "test_func"

            wrapper = is_owner(test_func)

            response = wrapper()

            # Logout as owner
            self.logout()

        self.assertEqual(response, test_func())

        # Go ahead to ensure that admin cannot run the function
        with self.test_app:
            # Login as admin
            self.login(
                email=self.admin_email,
                password=self.admin_password
            )
            # Select business
            self.select_business(self.business_id)

            def test_func():
                return "test_func"

            wrapper = is_owner(test_func)

            response = wrapper()

            # Logout as admin
            self.logout()

        self.assertNotEqual(response, test_func())

        # Go ahead to ensure that cashier cannot run the function
        with self.test_app:
            # Login as cashier
            self.login(
                email=self.cashier_email,
                password=self.cashier_password
            )
            # Select business
            self.select_business(self.business_id)

            def test_func():
                return "test_func"

            wrapper = is_owner(test_func)

            response = wrapper()

            # Logout as cashier
            self.logout()

        self.assertNotEqual(response, test_func())


if __name__ == "__main__":
    unittest.main()
