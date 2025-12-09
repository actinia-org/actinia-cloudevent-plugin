#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2018-2025 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: GPL-3.0-or-later

Add endpoints to flask app with endpoint definitions and routes
"""

__license__ = "GPL-3.0-or-later"
__author__ = "Carmen Tawalika, Anika Weinmann, Lina Krisztian"
__copyright__ = "Copyright 2022-2024 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from flask_restful_swagger_2 import Api

from actinia_cloudevent_plugin.api.cloudevents import Cloudevent
from actinia_cloudevent_plugin.api.hooks import Hooks


# endpoints loaded if run as actinia-core plugin as well as standalone app
def create_endpoints(flask_api: Api) -> None:
    """Create plugin endpoints."""
    apidoc = flask_api
    apidoc.add_resource(Cloudevent, "/")
    apidoc.add_resource(Hooks, "/hooks/<string:source_name>")
