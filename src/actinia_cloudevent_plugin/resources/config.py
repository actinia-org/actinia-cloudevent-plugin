#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2025 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: Apache-2.0

Configuration file
"""

__author__ = "Carmen Tawalika, Lina Krisztian"
__copyright__ = "2018-2025 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


import configparser
from pathlib import Path

# config can be overwritten by mounting *.ini files into folders inside
# the config folder.
DEFAULT_CONFIG_PATH = "config"
CONFIG_FILES = [
    str(f) for f in Path(DEFAULT_CONFIG_PATH).glob("**/*.ini") if f.is_file()
]
GENERATED_CONFIG = DEFAULT_CONFIG_PATH + "/actinia-cloudevent-plugin.cfg"


class ACTINIA:
    """Default config for actinia processing."""

    enqueue_job_base_url = "http://localhost:8088/"
    use_actinia_modules = True
    user = "actinia-gdi"
    password = "actinia-gdi"
    worker_http_launcher_url = "http://localhost:8000/launch"


class EVENTRECEIVER:
    """Default config for cloudevent receiver."""

    url = "http://localhost:3000/"


class LOGCONFIG:
    """Default config for logging."""

    logfile = "actinia-cloudevent-plugin.log"
    level = "INFO"
    type = "stdout"


class Configfile:
    """Configuration file."""

    def __init__(self) -> None:
        """Overwrite config classes.

        Will overwrite the config classes above when config files
        named DEFAULT_CONFIG_PATH/**/*.ini exist.
        On first import of the module it is initialized.
        """
        config = configparser.ConfigParser()
        config.read(CONFIG_FILES)
        if len(config) <= 1:
            print("Could not find any config file, using default values.")
            return
        print("Loading config files: " + str(CONFIG_FILES) + " ...")

        with open(  # noqa: PTH123
            GENERATED_CONFIG,
            "w",
            encoding="utf-8",
        ) as configfile:
            config.write(configfile)
        print("Configuration written to " + GENERATED_CONFIG)

        # ACTINIA
        if config.has_section("ACTINIA"):
            if config.has_option("ACTINIA", "enqueue_job_base_url"):
                ACTINIA.enqueue_job_base_url = config.get(
                    "ACTINIA",
                    "enqueue_job_base_url",
                )
            if config.has_option("ACTINIA", "use_actinia_modules"):
                ACTINIA.use_actinia_modules = config.getboolean(
                    "ACTINIA",
                    "use_actinia_modules",
                )
            if config.has_option("ACTINIA", "user"):
                ACTINIA.user = config.get("ACTINIA", "user")
            if config.has_option("ACTINIA", "password"):
                ACTINIA.password = config.get("ACTINIA", "password")
            if config.has_option("ACTINIA", "worker_http_launcher_url"):
                ACTINIA.worker_http_launcher_url = config.get(
                    "ACTINIA",
                    "worker_http_launcher_url",
                )
        # LOGGING
        if config.has_section("LOGCONFIG"):
            if config.has_option("LOGCONFIG", "logfile"):
                LOGCONFIG.logfile = config.get("LOGCONFIG", "logfile")
            if config.has_option("LOGCONFIG", "level"):
                LOGCONFIG.level = config.get("LOGCONFIG", "level")
            if config.has_option("LOGCONFIG", "type"):
                LOGCONFIG.type = config.get("LOGCONFIG", "type")

        # EVENTRECEIVER
        if config.has_section("EVENTRECEIVER"):
            if config.has_option("EVENTRECEIVER", "url"):
                EVENTRECEIVER.url = config.get("EVENTRECEIVER", "url")


init = Configfile()
