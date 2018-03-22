import unittest

from POS.models.base_model import AppDB
from POS.models.user import User
from POS.user.signup.controllers import SignUp


class TestSignUp(unittest.TestCase):

    def setUp(self):
        self.user = User(
            name="temp_guy",
            email="temp_guy@gmail.com",
            password="temp_guy_pw"
        )

        AppDB.db_session.add(self.user)
        AppDB.db_session.commit()

    def test_user_exists(self):
        self.assertEqual(
            SignUp.user_exists(self.user.email),
            True
        )

    def tearDown(self):
        AppDB.db_session.delete(self.user)
        AppDB.db_session.commit()


if __name__ == "__main__":
    unittest.main()
