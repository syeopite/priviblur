import sys
import tomllib

from typing import NamedTuple

from . import deployment, priviblur_backend, cache_config, user_preferences, logging_config, misc


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
    default_user_preferences: user_preferences.DefaultUserPreferences
    cache: cache_config.CacheConfig
    logging: logging_config.LoggingConfig
    misc: misc.MiscellaneousConfig


def load_config(path : str) -> PriviblurConfig:
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

    # The config file can contain additional arguments that Priviblur does not recognize.
    # As such some processing is needed to only retrieve what Priviblur can understand
    
    # Defines config sections
    config_sections = (
        # Corresponding object, internal name, section name in the config file
        (deployment.DeploymentConfig, "deployment", "deployment"),
        (priviblur_backend.PriviblurBackendConfig, "backend", "priviblur_backend"),
        (user_preferences.DefaultUserPreferences, "default_user_preferences", "default_user_preferences"),
        (cache_config.CacheConfig, "cache", "cache"),
        (logging_config.LoggingConfig, "logging", "logging"),
        (misc.MiscellaneousConfig, "misc", "misc")
    )

    priviblur_config_data = {}

    for section_definition in config_sections:
        section_object, internal_name, external_name = section_definition
        arguments_to_load = {}
        arguments_from_config = config.get(external_name, {})

        # Ignore unknown config fields
        for k, v in arguments_from_config.items():
            if k in section_object._fields:
                arguments_to_load[k] = v

        priviblur_config_data[internal_name] = section_object(**arguments_to_load)

    # TODO Validate invalid config values

    return PriviblurConfig(
        **priviblur_config_data
    )


