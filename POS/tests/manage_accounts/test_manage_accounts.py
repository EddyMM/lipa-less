import unittest
import json

from POS.models.base_model import AppDB
from POS.models.business import Business
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

        from POS.models.role import Role
        AppDB.load_default_roles(Role)

    def tearDown(self):
        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()

    def test_add_role(self):
        # Add at least 2 users (one being the owner of a business)

        # random user
        random_user_name = "lipaless_user"
        random_user_email = "lipaless_user@gmail.com"
        random_user_password = "lipaless_pw"
        self.signup(
            name=random_user_name,
            email=random_user_email,
            password=random_user_password
        )
        # logout
        self.logout()

        # Owner
        owner_email = "lipaless_owner@gmail.com"
        self.signup(
            name="lipaless_owner",
            email=owner_email,
            password="lipaless_pw"
        )

        # create business that links the users
        business_name = "lipaless_business"
        self.create_business(
            name=business_name,
            contact_number="0712345678"
        )

        # Attempt to add the user to business as a cashier
        rv = self.add_user_role(
            role_name="cashier",
            email=random_user_email
        )

        assert b"200" in rv.data

        # Reverse roles to ensure normal user cannot assign roles
        self.logout()

        # 2nd normal user
        normal_user_email = "lipaless_2@gmail.com"
        self.signup(
            name="lipaless_2",
            email=normal_user_email,
            password="lipaless_2_pw"
        )

        self.logout()

        # Login the 1st normal user
        self.login(random_user_email, random_user_password)

        # Select business (only one has been created so id is 1)
        business = AppDB.db_session.query(Business).filter(
            Business.name == business_name
        ).first()
        self.select_business(business.id)

        # Attempt to add the user to business as a cashier
        rv = self.add_user_role(
            role_name="cashier",
            email=normal_user_email
        )

        print("rv.data: %s" % rv.data)
        # Should redirect user to select another business
        assert "303" in rv.status

    def test_modify_role(self):
        pass

    def signup(self, name, email, password):
        return self.test_app.post(
            "/signup",
            data=json.dumps(dict(
                name=name,
                email=email,
                password=password)),
            content_type="application/json"
        )

    def create_business(self, name, contact_number):
        return self.test_app.post(
            "/business",
            data=json.dumps({
                "name": name,
                "contact-number": contact_number
            }),
            content_type="application/json"
        )

    def login(self, email, password):
        return self.test_app.post(
            "/login",
            data=json.dumps(dict(
                email=email,
                password=password
            )),
            content_type="application/json"
        )

    def logout(self):
        return self.test_app.get("/logout")

    def select_business(self, business_id):
        return self.test_app.get("/business/select/%s" % business_id)

    def add_user_role(self, role_name, email):
        return self.test_app.post(
            "/manage_accounts/role",
            data=json.dumps({
                "role": role_name,
                "email": email
            }),
            content_type="application/json"
        )


if __name__ == "__main__":
    unittest.main()
