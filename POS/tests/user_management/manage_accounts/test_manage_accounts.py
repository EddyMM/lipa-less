import unittest

from POS.models.base_model import AppDB
from POS.models.user_management.business import Business
from POS.models.user_management.user import User
from POS.models.user_management.role import Role
from POS.models.user_management.user_business import UserBusiness
from POS.tests.user_management.base.base_test_case import BaseTestCase


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

        # Should work so expect 2 users in the DB
        self.assertTrue(len(AppDB.db_session.query(UserBusiness).filter(
            UserBusiness.business_id == business.id
        ).all()) == 2)

        # Reverse roles to ensure normal user cannot add roles
        # Logout as owner
        self.logout()

        # Create user #2 (without creating a business)
        self.user_2_email = "lipaless_2@gmail.com"
        self.signup(
            name="lipaless_2",
            email=self.user_2_email,
            password="lipaless_2_pw"
        )

        # Logout from user #2
        self.logout()

        # Login as user #1 who is a cashier
        self.login(self.user_1_email, self.user_1_password)

        # Select business
        self.select_business(self.business_1_id)

        # Attempt to add user #2 to business as a cashier
        self.add_user_role(
            role_name="cashier",
            email=self.user_2_email
        )

        # Logout as user #1
        self.logout()

        # Should be impossible to add user #2 using a cashier account so still 2 roles in the business should exist
        self.assertTrue(len(AppDB.db_session.query(UserBusiness).filter(
            UserBusiness.business_id == business.id
        ).all()) == 2)

        # Confirm that the owner of business #2 cannot add a role to business #1 where he is not an owner
        # Login as user #1
        self.login(self.user_1_email, self.user_1_password)

        # Create business #2 (So user #1 becomes owner of business #2)
        self.business_2_name = "lipaless_2_business"
        self.add_business(self.business_2_name, "0712524536")

        # Add user #2 to business #1 yet current logged in user(user #1) is not the owner
        self.add_user_role("cashier", self.user_2_email)

        # Confirm that it didn't work
        self.assertTrue(
            len(AppDB.db_session.query(UserBusiness).filter(
                UserBusiness.business_id == self.business_1_id
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
        rv = self.modify_user_role(
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
