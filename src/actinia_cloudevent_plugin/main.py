#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2025 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Application entrypoint. Creates Flask app and swagger docs, adds endpoints
"""

__author__ = "Carmen Tawalika, Lina Krisztian"
__copyright__ = "2025-present mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api

from actinia_cloudevent_plugin.endpoints import create_endpoints
from actinia_cloudevent_plugin.resources.logging import log

flask_app = Flask(__name__)
# allows endpoints with and without trailing slashes
flask_app.url_map.strict_slashes = False
CORS(flask_app)


API_VERSION = "v1"

URL_PREFIX = f"/api/{API_VERSION}"

apidoc = Api(
    flask_app,
    title="actinia-cloudevent-plugin",
    # prefix=URL_PREFIX,
    api_version=API_VERSION,
    api_spec_url=f"{URL_PREFIX}/swagger",
    schemes=["https", "http"],
    consumes=["application/json"],
    description="""Receives cloudevent,
                   transforms it to an actinia process chain
                   and returns cloudevent back.
                   """,
)

create_endpoints(flask_api=apidoc)

if __name__ == "__main__":
    # call this for development only with:
    # `python3 -m actinia_cloudevent_plugin.main`
    log.debug("starting app in development mode...")
    # ruff: S201 :Use of `debug=True` in Flask app detected
    flask_app.run(debug=True, use_reloader=False)  # noqa: S201
    # for production environent use application in wsgi.py
