import unittest
import json

from POS.models.base_model import AppDB
from POS.models.business import Business

from POS.tests.base.base_test_case import BaseTestCase


class TestLogin(BaseTestCase):
    def setUp(self):
        TestLogin.confirm_app_in_testing_mode()

        from POS import app
        app.testing = True
        app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
        self.test_app = app.test_client()

        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()
        AppDB.BaseModel.metadata.create_all()

        from POS.models.role import Role
        AppDB.load_default_roles(Role)

        # Business related  Requires one to have logged in to create a user first
        # Perform a signup
        test_name = "lipaless guy"
        test_email = "lipaless_guy@gmail.com"
        test_password = "lipaless_pw"

        self.signup(
            name=test_name,
            email=test_email,
            password=test_password
        )

    def tearDown(self):
        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()

    def test_get(self):
        rv = self.test_app.get("/business")
        assert b"Select business" in rv.data

    def test_post(self):
        test_business_name = "mandazi poa"
        test_contact_number = "0712345678"

        # Check if business can be created
        rv = self.add_business(
            name=test_business_name,
            contact_number=test_contact_number
        )
        assert b"Business created" in rv.data

        # Check if app detects business with same name
        self.add_business(
            name=test_business_name,
            contact_number=test_contact_number
        )

        self.assertTrue(AppDB.db_session.query(Business).count() == 1)

    def signup(self, name, email, password):
        return self.test_app.post(
            "/signup",
            data=json.dumps(dict(
                name=name,
                email=email,
                password=password)),
            content_type="application/json"
        )

    def add_business(self, name, contact_number):
        return self.test_app.post(
            "/business",
            data=json.dumps({
                "name":name,
                "contact-number":contact_number
                }
            ),
            content_type="application/json"
        )


if __name__ == "__main__":
    unittest.main()
