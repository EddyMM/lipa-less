import os
import sys
import unittest
import json

from POS.models.base_model import AppDB

from POS.constants import APP_CONFIG_ENV_VAR, TESTING_CONFIG_VAR, TESTING_DATABASE_URL


class BaseTestCase(unittest.TestCase):
    @staticmethod
    def confirm_app_in_testing_mode():
        """
            Checks if the app is configured to be in testing mode.
            If not, exit since the env vars may be incorrect
        :return:
        """
        if os.getenv(APP_CONFIG_ENV_VAR, "") != TESTING_CONFIG_VAR or \
                not TESTING_DATABASE_URL:
            # TODO: Check for this in the setup
            print("Testing env vars not defined")
            sys.exit(0)

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

    def login_as_admin(self):
        # Login as an admin
        self.login(
            email=self.admin_email,
            password=self.admin_password
        )

        # Select business
        self.select_business(self.business_id)

    def login_as_cashier(self):
        self.login(
            self.cashier_email,
            self.cashier_password
        )

        # Select business
        self.select_business(self.business_id)

    def init_test_app(self):
        """
            Create the application test client
            and set up the database
            :return:
        """
        BaseTestCase.confirm_app_in_testing_mode()

        from POS import app
        app.testing = True
        app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
        self.test_app = app.test_client()

        # Initialize the database
        BaseTestCase.init_test_db()

    def tearDown(self):
        self.logout()
        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()

    @staticmethod
    def init_test_db():
        """
            Initialize the test database
            :return:
        """
        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()
        AppDB.BaseModel.metadata.create_all()

        from POS.models.user_management.role import Role
        AppDB.load_default_roles(Role)

    def signup(self, name, email, password):
        """
            Sign up a test user
            :param name:
            :param email:
            :param password:
            :return:
        """
        return self.send_json_post(
            "/signup",
            name=name,
            email=email,
            password=password
        )

    def add_business(self, name, contact_number):
        """
            Add a test business
            :param name:
            :param contact_number:
            :return:
        """
        return self.send_json_post(
            "/business",
            name=name,
            contact_number=contact_number
        )

    def add_user_role(self, role_name, email):
        """
            Add a new user role (e.g. cashier) to a test business
            :param role_name:
            :param email:
            :return:
        """
        return self.send_json_post(
            endpoint="/manage_accounts/role",
            role=role_name,
            email=email
        )

    def modify_user_role(self, emp_id, role, deactivated):
        """
            Alter the role or deactivation status of a user in a business
            :param emp_id:
            :param role:
            :param deactivated:
            :return:
        """
        return self.send_json_put(
            endpoint="/manage_accounts/role",
            roles=[{
                    "emp_id": emp_id,
                    "role": role,
                    "deactivated": deactivated
                }]
        )

    def select_business(self, business_id):
        """
            Specify the business a test user is logging in to
            :param business_id:
            :return:
        """
        return self.test_app.get("/business/select/%s" % business_id)

    def login(self, email, password):
        """
            Log in a test user
            :param email:
            :param password:
            :return:
        """
        return self.send_json_post(
            endpoint="/login",
            email=email,
            password=password
        )

    def logout(self):
        """
            Log out a test user
            :return:
        """
        return self.test_app.get("/logout")

    def send_json_post(self, endpoint: str, **kwargs):
        """
            Package a list of keyword args into JSON and send them as a POST
            test request
            :param endpoint:
            :param kwargs:
            :return:
        """
        return self.test_app.post(
            endpoint,
            data=json.dumps(kwargs),
            content_type="application/json"
        )

    def send_json_put(self, endpoint: str, **kwargs):
        """
            Package a list of keyword args into JSON and send them as a PUT
            test request
            :param endpoint:
            :param kwargs:
            :return:
        """
        return self.test_app.put(
            endpoint,
            data=json.dumps(kwargs),
            content_type="application/json"
        )

    def send_json_delete(self, endpoint: str, **kwargs):
        """
            Package a list of keyword args into JSON and send them as a DELETE
            test request
            :param endpoint:
            :param kwargs:
            :return:
        """
        return self.test_app.delete(
            endpoint,
            data=json.dumps(kwargs),
            content_type="application/json"
        )
