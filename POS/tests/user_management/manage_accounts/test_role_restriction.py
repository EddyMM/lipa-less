import unittest

from POS.models.base_model import AppDB
from POS.tests.user_management.base.base_test_case import BaseTestCase
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

    def create_users(self):
        """
            Create an owner, admin and cashier
        :return:
        """
        # Create owner
        self.create_owner()

        # Create admin
        self.create_admin()

        # Create cashier
        self.create_cashier()

    def create_owner(self):
        """
            Creates an owner role
        :return:
        """
        # Create user
        self.owner_name = "owner"
        self.owner_email = "owner@gmail.com"
        self.owner_password = "owner_pw"

        self.signup(
            name=self.owner_name,
            email=self.owner_email,
            password=self.owner_password
        )

        # Create business which associates this user with business
        # making him/her the owner
        self.create_business()

        with self.test_app as c:
            with c.session_transaction() as sess:
                self.business_id = sess["business_id"]

        # logout as owner
        self.logout()

    def create_business(self):
        """
            Creates the test business
        :return:
        """
        self.business_name = "test_business"
        contact_number = "0712345678"

        self.add_business(
            name=self.business_name,
            contact_number=contact_number
        )

    def create_admin(self):
        # Create user
        self.admin_name = "admin"
        self.admin_email = "admin@gmail.com"
        self.admin_password = "admin_pw"

        self.signup(
            name=self.admin_name,
            email=self.admin_email,
            password=self.admin_password
        )

        # logout as potential admin
        self.logout()

        # Login as owner
        self.login(
            email=self.owner_email,
            password=self.owner_password
        )

        # Associate owner with business
        self.select_business(self.business_id)

        # Set the admin user as 'admin'
        self.add_user_role(
            role_name="admin",
            email=self.admin_email
        )

        # Logout as owner
        self.logout()

    def create_cashier(self):
        # Create user
        self.cashier_name = "cashier"
        self.cashier_email = "cashier@gmail.com"
        self.cashier_password = "cashier_pw"

        self.signup(
            name=self.cashier_name,
            email=self.cashier_email,
            password=self.cashier_password
        )

        # logout as potential cashier
        self.logout()

        # Login as owner
        self.login(
            email=self.owner_email,
            password=self.owner_password
        )

        # Associate owner with business
        self.select_business(self.business_id)

        # Set the user as 'admin'
        self.add_user_role(
            role_name="cashier",
            email=self.cashier_email
        )

        # Logout as owner
        self.logout()

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

        self.assertEquals(response, test_func())

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

        self.assertEquals(response, test_func())

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

        self.assertNotEquals(response, test_func())

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

        self.assertEquals(response, test_func())

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

        self.assertNotEquals(response, test_func())

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

        self.assertNotEquals(response, test_func())


if __name__ == "__main__":
    unittest.main()
