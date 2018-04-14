import unittest

from POS.models.base_model import AppDB
from POS.models.user_management.business import Business
from POS.models.user_management.user import User

from POS.tests.base.base_test_case import BaseTestCase


class TestBusiness(BaseTestCase):
    def setUp(self):
        TestBusiness.confirm_app_in_testing_mode()

        from POS import app
        app.testing = True
        app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
        self.test_app = app.test_client()

        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()
        AppDB.BaseModel.metadata.create_all()

        from POS.models.user_management.role import Role
        AppDB.load_default_roles(Role)

        # Business details
        self.test_business_name = "mandazi poa"
        self.test_contact_number = "0712345678"

        # Business related functionality requires one to have logged in so create users

        # Perform a signup
        self.user_1_name = "lipaless guy"
        self.user_1_email = "lipaless_guy@gmail.com"
        self.user_1_password = "lipaless_pw"

        self.signup(
            name=self.user_1_name,
            email=self.user_1_email,
            password=self.user_1_password
        )

        # Logout as user 1
        self.logout()

        # Sign up user 2
        self.user_2_name = "lipaless guy_2"
        self.user_2_email = "lipaless_guy_2@gmail.com"
        self.user_2_password = "lipaless_pw_2"

        self.signup(
            name=self.user_2_name,
            email=self.user_2_email,
            password=self.user_2_password
        )

        # Logout as user 2
        self.logout()

    def tearDown(self):
        self.logout()
        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()

    def test_get(self):
        self.login(self.user_1_email, self.user_1_password)

        rv = self.test_app.get("/business")
        assert b"Select business" in rv.data

    def test_post(self):
        self.login(self.user_1_email, self.user_1_password)

        # Check if business can be created
        rv = self.add_business(
            name=self.test_business_name,
            contact_number=self.test_contact_number
        )
        assert b"Business created" in rv.data

        # Check if app detects business with same name
        self.add_business(
            name=self.test_business_name,
            contact_number=self.test_contact_number
        )

        self.assertTrue(AppDB.db_session.query(Business).count() == 1)

    def test_deactivated_user_in_business(self):
        # Login user 1
        self.login(self.user_1_email, self.user_1_password)

        # Create business hence user 1 is owner
        self.add_business(
            name=self.test_business_name,
            contact_number=self.test_contact_number
        )

        # Add user 2 to business
        self.add_user_role("admin", self.user_2_email)

        # Deactivate user 2
        # First get user 2's id
        user_2 = AppDB.db_session.query(User).filter(
            User.email == self.user_2_email
        ).first()

        self.modify_user_role(
            emp_id=user_2.emp_id,
            role="admin",
            deactivated=True
        )

        # Logout as user 1
        self.logout()

        # Login as user 2
        self.login(self.user_2_email, self.user_2_password)

        # Try selecting the business
        # First get the business id
        business = AppDB.db_session.query(Business).filter(
            Business.name == self.test_business_name
        ).first()

        rv = self.select_business(business.id)

        print(rv.data)

        # Check if it returns a 403 (Forbidden) response status
        self.assertIn(b"403", rv.data)


if __name__ == "__main__":
    unittest.main()
