import sys
import os
import unittest
import json

from POS.constants import APP_CONFIG_ENV_VAR, TESTING_CONFIG_VAR, TESTING_DATABASE_URL

from POS.models.base_model import AppDB
from POS.models.user import User
from POS.user.signup.controllers import SignUp

from POS import app


class TestSignUp(unittest.TestCase):
    def setUp(self):
        if os.getenv(APP_CONFIG_ENV_VAR, "") != TESTING_CONFIG_VAR or \
                not TESTING_DATABASE_URL:
            print("Testing env vars not defined")
            sys.exit(0)
        app.testing = True
        app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
        self.test_app = app.test_client()

        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()
        AppDB.BaseModel.metadata.create_all()

    def tearDown(self):
        AppDB.db_session.commit()
        AppDB.BaseModel.metadata.drop_all()

    def test_user_exists(self):
        self.user = User(
            name="temp_guy",
            email="temp_guy@gmail.com",
            password="temp_guy_pw"
        )

        AppDB.db_session.add(self.user)
        AppDB.db_session.commit()
        self.assertEqual(
            SignUp.user_exists(self.user.email),
            True
        )

    def test_get(self):
        rv = self.test_app.get("/signup")
        assert b"SIGN UP" in rv.data

    def test_post(self):
        # Perform a signup
        test_name = "lipaless guy"
        test_email = "lipaless_guy@gmail.com"
        test_password = "lipaless_pw"
        
        rv = self.signup(
            name=test_name,
            email=test_email,
            password=test_password
        )
        assert b"User created" in rv.data
        
        # Try signing up again to confirm it
        # detects you're already signed up
        rv = self.signup(
            name=test_name,
            email=test_email,
            password=test_password
        )
        assert b"already exists" in rv.data

    def signup(self, name, email, password):
        return self.test_app.post(
            "/signup",
            data=json.dumps(dict(
                name=name,
                email=email,
                password=password)),
            content_type="application/json"
        )


if __name__ == "__main__":
    unittest.main()
