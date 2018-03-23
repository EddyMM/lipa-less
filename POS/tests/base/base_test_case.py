import os
import sys
import unittest

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
