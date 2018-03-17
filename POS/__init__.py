import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, send_from_directory

from .home.controllers import home_bp
from .user.signup.controllers import signup_bp
from .user.login.controllers import login_bp
from .utils import get_config_type
from .constants import DEV_CONFIG_VAR, PROD_CONFIG_VAR, APP_NAME


def config_app(app_instance):
    """
    Sets the app_instance configurations in the order of:
        - Check ENV VAR
        - Load configuration object
        - Load configuration file
    The order of precedence is thus bottom-up

    Args:
        - app_instance: An instance of Flask
    """

    config_type = get_config_type()

    # Possible configurations as a dictionary
    configs = {
        DEV_CONFIG_VAR: "POS.config.DevelopmentConfig",
        PROD_CONFIG_VAR: "POS.config.ProductionConfig"
    }

    app_instance.config.from_object(configs[config_type])

    config_file_path = os.environ.get(APP_NAME + "_APP_CONFIG_FILE", "")

    if config_file_path and os.path.exists(config_file_path):
        app_instance.config.from_pyfile(config_file_path)


def set_up_logging(app_instance):
    """
    Establish logging techniques for the app when in production
    """
    app_instance.logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(APP_NAME + ".log")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("[%(asctime)s][%(levelname)s]: %(message)s"))

    app_instance.logger.addHandler(handler)


def init_app(app_instance):
    """
    Initialize the application (configuration, logging, ...)
    :param app_instance: Flask app instance
    :return:
    """
    # Configure the app
    config_app(app_instance)

    # Set up logging
    set_up_logging(app)


app = Flask(__name__)
init_app(app)


@app.route("/favicon.ico")
def favicon():
    """
        Browsers request for a favicon.ico file as the icon to use for the page
        This controller will handle this request from the browser
        :return:  App icon
    """
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico'
    )


# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
