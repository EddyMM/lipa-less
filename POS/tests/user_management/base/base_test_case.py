import os
import sys
import unittest
import json

from flask import logging

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
            logging.getLogger().log(
                logging.ERROR,
                "Testing env vars not defined")
            sys.exit(0)

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

    def add_user_role(self, role_name, email):
        return self.test_app.post(
            "/manage_accounts/role",
            data=json.dumps({
                "role": role_name,
                "email": email
            }),
            content_type="application/json"
        )

    def modify_user_role(self, emp_id, role, deactivated):
        return self.test_app.put(
            "/manage_accounts/role",
            data=json.dumps({
                "roles": [{
                    "emp_id": emp_id,
                    "role": role,
                    "deactivated": deactivated
                }]
            }),
            content_type="application/json"
        )

    def select_business(self, business_id):
        return self.test_app.get("/business/select/%s" % business_id)

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