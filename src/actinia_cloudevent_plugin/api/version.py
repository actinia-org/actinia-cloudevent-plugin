#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2025 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: GPL-3.0-or-later

Version information
"""

__license__ = "GPL-3.0-or-later"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2025 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"

import os
import sys
from importlib import metadata

from flask import jsonify, make_response
from flask_restful_swagger_2 import Resource


class Version(Resource):
    """Version information."""

    def get(self):
        """Get version information."""
        info = {}

        plugin_name = __package__.split(".")[0]
        info["version"] = metadata.version(plugin_name)

        python_version = sys.version.replace("\n", "- ")
        info["python_version"] = python_version

        env_name = "RUNNING_SINCE"
        if env_name in os.environ:
            info["running_since"] = os.environ[env_name]
        else:
            info["running_since"] = "n/a"

        return make_response(jsonify(info), 200)
