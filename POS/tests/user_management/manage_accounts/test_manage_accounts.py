import unittest

from POS.models.base_model import AppDB
from POS.models.user_management.business import Business
from POS.models.user_management.user import User
from POS.models.user_management.role import Role
from POS.models.user_management.user_business import UserBusiness
from POS.tests.base.base_test_case import BaseTestCase


class TestManageAccounts(BaseTestCase):
    def setUp(self):
        TestManageAccounts.confirm_app_in_testing_mode()

        from POS import app
        app.testing = True
        app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
        self.test_app = app.test_client()

        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()
        AppDB.BaseModel.metadata.create_all()

        from POS.models.user_management.role import Role
        AppDB.load_default_roles(Role)

        # Add at least 2 users (one being the owner of a business)

        # user #1 details
        self.user_1_name = "lipaless_user"
        self.user_1_email = "lipaless_user@gmail.com"
        self.user_1_password = "lipaless_pw"

        # signup as user #1
        self.signup(
            name=self.user_1_name,
            email=self.user_1_email,
            password=self.user_1_password
        )
        # logout as user #1
        self.logout()

        # Signup as owner
        self.owner_name = "lipaless_owner"
        self.owner_email = "lipaless_owner@gmail.com"
        self.owner_password = "lipaless_pw"

        self.signup(
            name=self.owner_name,
            email=self.owner_email,
            password=self.owner_password
        )

        # create business #1 that links the users
        self.business_1_name = "lipaless_business"
        self.add_business(
            name=self.business_1_name,
            contact_number="0712345678"
        )

        business_1 = AppDB.db_session.query(Business).filter(
            Business.name == self.business_1_name
        ).first()
        self.business_1_id = business_1.id

        # logout as owner
        self.logout()

    def tearDown(self):
        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()

    def test_add_role(self):
        # Login as owner
        self.login(self.owner_email, self.owner_password)

        # Select business
        business = AppDB.db_session.query(Business).filter(
            Business.name == self.business_1_name
        ).first()
        self.select_business(business.id)

        # Add user #1 to business as a cashier
        self.add_user_role(
            role_name="cashier",
            email=self.user_1_email
        )

        # Logout as owner
        self.logout()

        # Should work so expect 2 users in the DB
        self.assertTrue(len(AppDB.db_session.query(UserBusiness).filter(
            UserBusiness.business_id == business.id
        ).all()) == 2)

    def test_modify_role(self):
        # Change user #1 to an admin
        # Login as owner of business #1
        self.login(self.owner_email, self.owner_password)

        # Select business #1
        self.select_business(self.business_1_id)

        # Add user #1 to business as a cashier
        self.add_user_role(
            role_name="cashier",
            email=self.user_1_email
        )

        # Get user #1 id
        user_1 = AppDB.db_session.query(User).filter(
            User.email == self.user_1_email
        ).first()
        user_1_id = user_1.emp_id

        # Modify user #1
        self.modify_user_role(
            emp_id=user_1_id,
            role="admin",
            deactivated=False
        )

        # Get user #1's role
        user_1_role = AppDB.db_session.query(UserBusiness).filter(
            UserBusiness.emp_id == user_1_id,
            UserBusiness.business_id == self.business_1_id
        ).first()
        admin_role_id = Role.get_role_id("admin")

        # Logout as owner
        self.logout()

        # Confirm that user #1's role is now admin
        self.assertEqual(admin_role_id, user_1_role.role_id)


if __name__ == "__main__":
    unittest.main()
