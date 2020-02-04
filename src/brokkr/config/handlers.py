"""
Config handler setup for Brokkr's main managed configs.
"""

# Local imports
import brokkr.config.base
from brokkr.config.constants import (
    CONFIG_NAME_BOOTSTRAP,
    CONFIG_NAME_DYNAMIC,
    CONFIG_NAME_LOG,
    CONFIG_NAME_METADATA,
    CONFIG_NAME_MODE,
    CONFIG_NAME_STATIC,
    CONFIG_NAME_SYSTEM,
    CONFIG_NAME_UNIT,
    LEVEL_NAME_REMOTE,
    LEVEL_NAME_SYSTEM,
    LEVEL_NAME_SYSTEM_CLIENT,
    OUTPUT_PATH_DEFAULT,
    OUTPUT_SUBPATH_LOG,
    OUTPUT_SUBPATH_MONITOR,
    PACKAGE_NAME,
    SYSTEM_SUBPATH_CONFIG,
    )
from brokkr.config.mode import MODE_CONFIG
from brokkr.config.system import SYSTEM_CONFIG
import brokkr.config.systemhandler


SYSTEM_CONFIG_PATH = SYSTEM_CONFIG["system_path"] / SYSTEM_SUBPATH_CONFIG
MODE_OVERLAY = MODE_CONFIG[MODE_CONFIG["mode"]]


DEFAULT_CONFIG_BOOTSTRAP = {
    "output_path_client": OUTPUT_PATH_DEFAULT.as_posix(),
    "system_prefix": "mjolnir",
    }
PATH_VARIABLES_BOOTSTRAP = [("output_path_client", )]

CONFIG_TYPE_BOOTSTRAP = brokkr.config.base.ConfigType(
    CONFIG_NAME_BOOTSTRAP,
    defaults=DEFAULT_CONFIG_BOOTSTRAP,
    preset_config_path=SYSTEM_CONFIG_PATH,
    path_variables=PATH_VARIABLES_BOOTSTRAP,
    )
CONFIG_LEVELS_BOOTSTRAP = [
    brokkr.config.base.FileConfigLevel(
        name=LEVEL_NAME_SYSTEM, config_type=CONFIG_TYPE_BOOTSTRAP,
        preset=True, append_level=False),
    brokkr.config.base.FileConfigLevel(
        name=LEVEL_NAME_SYSTEM_CLIENT, config_type=CONFIG_TYPE_BOOTSTRAP,
        preset=True),
    brokkr.config.base.FileConfigLevel(
        config_type=CONFIG_TYPE_BOOTSTRAP, append_level=False),
    ]
CONFIG_HANDLER_BOOTSTRAP = brokkr.config.base.ConfigHandler(
    config_type=CONFIG_TYPE_BOOTSTRAP,
    config_levels=CONFIG_LEVELS_BOOTSTRAP,
    overlay=MODE_OVERLAY.get(CONFIG_NAME_BOOTSTRAP, None),
    )


DEFAULT_CONFIG_UNIT = {
    "number": 0,
    "network_interface": "wlan0",
    "site_description": "",
    }

CONFIG_TYPE_UNIT = brokkr.config.base.ConfigType(
    CONFIG_NAME_UNIT,
    defaults=DEFAULT_CONFIG_UNIT,
    preset_config_path=SYSTEM_CONFIG_PATH,
    )
CONFIG_LEVELS_UNIT = [
    brokkr.config.base.FileConfigLevel(
        name=LEVEL_NAME_SYSTEM, config_type=CONFIG_TYPE_UNIT,
        preset=True, append_level=False),
    brokkr.config.base.FileConfigLevel(
        config_type=CONFIG_TYPE_UNIT, append_level=False),
    ]
CONFIG_HANDLER_UNIT = brokkr.config.base.ConfigHandler(
    config_type=CONFIG_TYPE_UNIT,
    config_levels=CONFIG_LEVELS_UNIT,
    overlay=MODE_OVERLAY.get(CONFIG_NAME_UNIT, None),
    )


EMPTY_VARS_METADATA = [
    "name_full", "author", "description", "homepage", "repo", "version"]
EMPTY_VARS_METADATA_DICT = {key: "" for key in EMPTY_VARS_METADATA}

DEFAULT_CONFIG_METADATA = {
    "name": "mjolnir",
    **EMPTY_VARS_METADATA_DICT,
    "brokkr_version_min": "0.3.0",
    "sindri_version_min": "0.3.0",
    }

CONFIG_TYPE_METADATA = brokkr.config.base.ConfigType(
    CONFIG_NAME_METADATA,
    defaults=DEFAULT_CONFIG_METADATA,
    preset_config_path=SYSTEM_CONFIG["system_path"],
    )
CONFIG_LEVELS_METADATA = [
    brokkr.config.base.FileConfigLevel(
        name=LEVEL_NAME_SYSTEM, config_type=CONFIG_TYPE_METADATA,
        preset=True, append_level=False),
    brokkr.config.base.FileConfigLevel(
        config_type=CONFIG_TYPE_METADATA, append_level=False),
    ]
CONFIG_HANDLER_METADATA = brokkr.config.base.ConfigHandler(
    config_type=CONFIG_TYPE_METADATA,
    config_levels=CONFIG_LEVELS_METADATA,
    overlay=MODE_OVERLAY.get(CONFIG_NAME_METADATA, None),
    )


LOG_FORMAT_DETAILED = ("{asctime}.{msecs:0>3.0f} | {levelname} | {name} | "
                       "{message} (T+{relativeCreated:.0f} ms)")
DEFAULT_LOG_LEVEL = "INFO"

DEFAULT_CONFIG_LOG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": LOG_FORMAT_DETAILED,
            "style": "{",
            },
        },
    "handlers": {
        "file": {
            "backupCount": 10,
            "class": "logging.handlers.RotatingFileHandler",
            "filename":
                (OUTPUT_SUBPATH_LOG
                 / (PACKAGE_NAME + "_{system_name}_{unit_number:0>2}.log"))
                .as_posix(),
            "formatter": "detailed",
            "level": DEFAULT_LOG_LEVEL,
            "maxBytes": int(1e7),
            },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": DEFAULT_LOG_LEVEL,
            "stream": "ext://sys.stdout",
            },
        },
    "root": {
        "handlers": ["file", "console"],
        "level": DEFAULT_LOG_LEVEL,
        },
    }

CONFIG_TYPE_LOG = brokkr.config.base.ConfigType(
    CONFIG_NAME_LOG,
    defaults=DEFAULT_CONFIG_LOG,
    config_version=None,
    preset_config_path=SYSTEM_CONFIG_PATH,
    )
CONFIG_LEVELS_LOG = [
    brokkr.config.base.FileConfigLevel(
        name=LEVEL_NAME_SYSTEM, config_type=CONFIG_TYPE_LOG,
        preset=True, append_level=False),
    brokkr.config.base.FileConfigLevel(
        name=LEVEL_NAME_SYSTEM_CLIENT, config_type=CONFIG_TYPE_LOG,
        preset=True),
    brokkr.config.base.FileConfigLevel(
        config_type=CONFIG_TYPE_LOG, append_level=False),
    ]
CONFIG_HANDLER_LOG = brokkr.config.base.ConfigHandler(
    config_type=CONFIG_TYPE_LOG,
    config_levels=CONFIG_LEVELS_LOG,
    overlay=MODE_OVERLAY.get(CONFIG_NAME_LOG, None),
    )


DEFAULT_CONFIG_STATIC = {
    "general": {
        "ip_sensor": "",
        "na_marker": "NA",
        "output_filename_client":
            "{output_type}_{system_name}_{unit_number:0>2}_{utc_date!s}.csv",
        },
    "link": {
        "local_port": 22,
        "server_hostname": "",
        "server_port": 22,
        "server_username": "",
        "tunnel_port_offset": 10000,
        },
    "monitor": {
        "filename_args": {"output_type": "telemetry"},
        "hs_port": 8084,
        "output_path_client": OUTPUT_SUBPATH_MONITOR.as_posix(),
        "sleep_interval_s": 0.5,
        "sunsaver_pid_list": [],
        "sunsaver_port": "",
        "sunsaver_start_offset": 0,
        "sunsaver_unit": 1,
        },
    }
PATH_VARIABLES_STATIC = [("monitor", "output_path_client")]

CONFIG_TYPE_STATIC = brokkr.config.base.ConfigType(
    CONFIG_NAME_STATIC,
    defaults=DEFAULT_CONFIG_STATIC,
    path_variables=PATH_VARIABLES_STATIC,
    preset_config_path=SYSTEM_CONFIG_PATH,
    )
CONFIG_LEVELS_STATIC = [
    brokkr.config.base.FileConfigLevel(
        name=LEVEL_NAME_SYSTEM, config_type=CONFIG_TYPE_STATIC,
        preset=True, append_level=False),
    brokkr.config.base.FileConfigLevel(
        name=LEVEL_NAME_SYSTEM_CLIENT, config_type=CONFIG_TYPE_STATIC,
        preset=True),
    brokkr.config.base.FileConfigLevel(
        config_type=CONFIG_TYPE_STATIC, append_level=False),
    ]
CONFIG_HANDLER_STATIC = brokkr.config.base.ConfigHandler(
    config_type=CONFIG_TYPE_STATIC,
    config_levels=CONFIG_LEVELS_STATIC,
    overlay=MODE_OVERLAY.get(CONFIG_NAME_STATIC, None),
    )


DEFAULT_CONFIG_DYNAMIC = {
    "monitor": {
        "monitor_interval_s": 60,
        "hs_timeout_s": 2,
        "ping_timeout_s": 1,
        },
    }

CONFIG_TYPE_DYNAMIC = brokkr.config.base.ConfigType(
    CONFIG_NAME_DYNAMIC,
    defaults=DEFAULT_CONFIG_DYNAMIC,
    preset_config_path=SYSTEM_CONFIG_PATH,
    )
CONFIG_LEVELS_DYNAMIC = [
    brokkr.config.base.FileConfigLevel(
        name=LEVEL_NAME_SYSTEM, config_type=CONFIG_TYPE_DYNAMIC,
        preset=True, append_level=False),
    brokkr.config.base.FileConfigLevel(
        name=LEVEL_NAME_SYSTEM_CLIENT, config_type=CONFIG_TYPE_DYNAMIC,
        preset=True),
    brokkr.config.base.FileConfigLevel(
        name=LEVEL_NAME_REMOTE, config_type=CONFIG_TYPE_DYNAMIC,
        extension=brokkr.config.base.EXTENSION_JSON),
    brokkr.config.base.FileConfigLevel(config_type=CONFIG_TYPE_DYNAMIC),
    ]
CONFIG_HANDLER_DYNAMIC = brokkr.config.base.ConfigHandler(
    config_type=CONFIG_TYPE_DYNAMIC,
    config_levels=CONFIG_LEVELS_DYNAMIC,
    overlay=MODE_OVERLAY.get(CONFIG_NAME_DYNAMIC, None),
    )


CONFIG_HANDLERS = {
    CONFIG_NAME_METADATA: CONFIG_HANDLER_METADATA,
    CONFIG_NAME_BOOTSTRAP: CONFIG_HANDLER_BOOTSTRAP,
    CONFIG_NAME_UNIT: CONFIG_HANDLER_UNIT,
    CONFIG_NAME_LOG: CONFIG_HANDLER_LOG,
    CONFIG_NAME_STATIC: CONFIG_HANDLER_STATIC,
    CONFIG_NAME_DYNAMIC: CONFIG_HANDLER_DYNAMIC,
    }
CONFIG_LEVEL_NAMES = {
    config_level.name for handler in CONFIG_HANDLERS.values()
    for config_level in handler.config_levels.values()}

ALL_CONFIG_HANDLERS = {
    **{CONFIG_NAME_SYSTEM:
       brokkr.config.systemhandler.CONFIG_HANDLER_SYSTEM},
    **{CONFIG_NAME_MODE:
       brokkr.config.modehandler.CONFIG_HANDLER_MODE},
    **CONFIG_HANDLERS,
    }
ALL_CONFIG_LEVEL_NAMES = {
    config_level.name for handler in ALL_CONFIG_HANDLERS.values()
    for config_level in handler.config_levels.values()}
