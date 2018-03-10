import os
from .constants import APP_NAME, DEV_CONFIG_VAR


def get_config_type():
    return os.environ.get(APP_NAME + "_CONFIG", DEV_CONFIG_VAR).lower().strip()
