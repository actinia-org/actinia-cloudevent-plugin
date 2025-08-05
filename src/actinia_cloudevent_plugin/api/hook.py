#!/usr/bin/env python
"""Copyright (c) 2025 mundialis GmbH & Co. KG.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Hello World class
"""

__license__ = "GPLv3"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2025 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"

import json

import requests
from cloudevents.conversion import to_binary
from cloudevents.http import CloudEvent
from flask import jsonify, make_response, request
from flask_restful_swagger_2 import Resource, swagger

from actinia_cloudevent_plugin.apidocs import hook
from actinia_cloudevent_plugin.model.response_models import (
    SimpleStatusCodeResponseModel,
)
from actinia_cloudevent_plugin.resources.config import EVENTRECEIVER


class Hook(Resource):
    """Webhook handling."""

    def get(self, source_name):
        """Cloudevent get method: not allowed response."""
        _source_name = source_name
        res = jsonify(
            SimpleStatusCodeResponseModel(
                status=405,
                message="Method Not Allowed",
            ),
        )
        return make_response(res, 405)

    def head(self, source_name):
        """Cloudevent head method: return empty response."""
        _source_name = source_name
        return make_response("", 200)

    @swagger.doc(hook.describe_hook_post_docs)
    def post(self, source_name) -> SimpleStatusCodeResponseModel:
        """Translate actinia webhook call to cloudevent.

        This method is called by HTTP POST actinia-core webhook
        """
        # only actinia as source supported so far
        if source_name != "actinia":
            return make_response(
                jsonify(
                    SimpleStatusCodeResponseModel(
                        status=400,
                        message="Bad Request: Source name not 'actinia'",
                    ),
                ),
                400,
            )

        postbody = request.get_json(force=True)

        if type(postbody) is dict:
            postbody = json.dumps(postbody)
        elif not isinstance(postbody, str):
            postbody = str(postbody)

        resp = json.loads(postbody)
        if "resource_id" not in resp:
            return make_response(
                jsonify(
                    SimpleStatusCodeResponseModel(
                        status=400,
                        message="Bad Request: No resource_id found in request",
                    ),
                ),
                400,
            )

        # TODO: define when to send cloudevent
        status = resp["status"]
        if status == "finished":
            # TODO send cloudevent
            pass
        terminate_status = ["finished", "error", "terminated"]
        if status in terminate_status:
            # TODO send cloudevent
            pass

        # TODO: move to common function from core.cloudevents
        url = EVENTRECEIVER.url
        try:
            attributes = {
                "specversion": "1.0",
                "source": "/actinia-cloudevent-plugin",
                "type": "com.mundialis.actinia.process.status",
                "subject": "nc_spm_08/PERMANENT",
                "datacontenttype": "application/json",
            }
            data = {"actinia_job": resp}
            event = CloudEvent(attributes, data)
            headers, body = to_binary(event)
            requests.post(url, headers=headers, data=body)
        except ConnectionError as e:
            return f"Connection ERROR when returning cloudevent: {e}"
        except Exception() as e:
            return f"ERROR when returning cloudevent: {e}"

        res = jsonify(
            SimpleStatusCodeResponseModel(
                status=200,
                message="Thank you for your update",
            ),
        )
        return make_response(res, 200)
