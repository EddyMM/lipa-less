import os
from .constants import APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR


def get_config_type():
    return os.environ.get(APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR).lower().strip()
