import sys
import tomllib

from typing import NamedTuple

from . import deployment, priviblur_backend, logging_config, misc


class PriviblurConfig(NamedTuple):
    """NamedTuple storing configuration data for Priviblur

    Encapsulates various configuration settings under a single field.

    Attributes:
        deployment: Configuration settings for deploying Priviblur
        backend: Configuration settings to customize 
            how Priviblur requests Tumblr
        logging: Configuration settings to change logging behavior
        misc: Configuration settings that doesn't fit into any other categories
    """

    deployment: deployment.DeploymentConfig
    backend: priviblur_backend.PriviblurBackendConfig
    logging: logging_config.LoggingConfig
    misc: misc.MiscellaneousConfig


def load_config(path : str):
    """Loads a TOML configuration file into a PriviblurConfig object"""

    try:
        with open(path, "rb") as config_file:
            config = tomllib.load(config_file)
    except FileNotFoundError:
        print(
            'Cannot find configuration file at "./config.toml". '
            'Did you mean to set a new location with the environmental variable "PRIVIBLUR_CONFIG_LOCATION"?'
        )
        sys.exit()
    except PermissionError:
        print("Cannot access the configuration file. Do I have the right permissions?")
        sys.exit()

    return PriviblurConfig(
        deployment=deployment.DeploymentConfig(**config["deployment"]),
        backend=priviblur_backend.PriviblurBackendConfig(**config["priviblur_backend"]),
        logging=logging_config.LoggingConfig(**config["logging"]),
        misc=misc.MiscellaneousConfig(**config["misc"])
    )


