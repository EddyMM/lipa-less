import os

# App
APP_NAME = "LipaLess"
DEV_CONFIG_VAR = "dev"
PROD_CONFIG_VAR = "prod"

# Database
DATABASE_URL_ENV_NAME = APP_NAME + "_DATABASE_URL"
DATABASE_URL = os.getenv(DATABASE_URL_ENV_NAME)

# Roles
OWNER_ROLE_NAME = "owner"
ADMIN_ROLE_NAME = "admin"
CASHIER_ROLE_NAME = "cashier"
