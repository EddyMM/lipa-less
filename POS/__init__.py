import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, send_from_directory, redirect, url_for, render_template
from flask_login import LoginManager
from flask_session import Session

from .home.controllers import home_bp
from .user.signup.controllers import signup_bp
from .user.login.controllers import login_bp
from .business.controllers import business_bp
from .dashboard.controllers import dashboard_bp
from .user.logout.controllers import logout_bp
from .manage_accounts.controllers import manage_accounts_bp

from .models.base_model import  AppDB
from .models.user import User

from .utils import get_config_type
from .constants import DEV_CONFIG_VAR, PROD_CONFIG_VAR,\
    TESTING_CONFIG_VAR, APP_NAME, OWNER_ROLE_NAME, ADMIN_ROLE_NAME, CASHIER_ROLE_NAME


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
        PROD_CONFIG_VAR: "POS.config.ProductionConfig",
        TESTING_CONFIG_VAR: "POS.config.TestingConfig"
    }

    app_instance.config.from_object(configs[config_type])

    config_file_path = os.environ.get(APP_NAME + "_APP_CONFIG_FILE", "")

    if config_file_path and os.path.exists(config_file_path):
        app_instance.config.from_pyfile(config_file_path)

    # Ensure flask doesn't redirect to trailing slash endpoint
    app_instance.url_map.strict_slashes = False


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

# Initialize the DB
with app.app_context():
    AppDB.init_db()

# Create login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_bp.login"

# Create session manager
ses = Session()
ses.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return AppDB.db_session.query(User).get(user_id)


@login_manager.unauthorized_handler
def unauthorized_access_callback():
    return redirect(url_for('login_bp.login'), code=303)


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


# Inject some important variables for templates to use
@app.context_processor
def inject_roles():
    return dict(
        OWNER_ROLE_NAME=OWNER_ROLE_NAME,
        ADMIN_ROLE_NAME=ADMIN_ROLE_NAME,
        CASHIER_ROLE_NAME=CASHIER_ROLE_NAME
    )


@app.errorhandler(400)
def error_400(error):
    return render_template("400-error.html")


@app.errorhandler(500)
def error_500(error):
    if error >= 500:
        return render_template("500-error.html")


# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(business_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(manage_accounts_bp)
