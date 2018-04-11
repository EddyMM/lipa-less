import unittest

from POS.models.base_model import AppDB

from POS.tests.user_management.base.base_test_case import BaseTestCase


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

    def tearDown(self):
        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()

    def test_get(self):
        rv = self.test_app.get("/login")
        assert b"LOG IN" in rv.data

    def test_post(self):
        from POS.models.user_management.user import User

        test_name = "lipaless"
        test_email = "lipaless@gmail.com"
        test_password = "lipaless_pw"

        # Create a user to test against
        # TODO: Create user from an SQL file
        AppDB.db_session.add(User(
            name=test_name,
            email=test_email,
            password=test_password
        ))

        AppDB.db_session.commit()

        # Test for email being empty
        rv = self.login("", test_password)
        assert b"Fill in" in rv.data

        # Test for password being empty
        rv = self.login(test_email, "")
        assert b"Fill in" in rv.data

        # Test for an email that exists and password is correct
        rv = self.login(test_email, test_password)
        assert b"Successful login" in rv.data

        # Test for an email that exists and password is wrong
        rv = self.login(test_email, test_password + "extra")
        assert b"Wrong password" in rv.data

        # Test for an email that doesn't exist in the first place
        rv = self.login(test_email + "extra", test_password)
        assert b"email not found" in rv.data


if __name__ == "__main__":
    unittest.main()
