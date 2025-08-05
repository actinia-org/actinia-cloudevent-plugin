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

from flask import jsonify, make_response, request
from flask_restful_swagger_2 import Resource, swagger

# from actinia_cloudevent_plugin.apidocs import webhook
from actinia_cloudevent_plugin.model.response_models import (
    SimpleStatusCodeResponseModel,
)


class Hook(Resource):
    """Webhook handling."""

    def get(self):
        """Cloudevent get method: not allowed response."""
        res = jsonify(
            SimpleStatusCodeResponseModel(
                status=405,
                message="Method Not Allowed",
            ),
        )
        return make_response(res, 405)

    # @swagger.doc(cloudevent.describe_cloudevent_post_docs)
    def post(self) -> SimpleStatusCodeResponseModel:
        """Translate actinia webhook call to cloudevent.

        This method is called by HTTP POST actinia-core webhook
        """

        postbody = request.get_json(force=True)

        if type(postbody) is dict:
            postbody = json.dumps(postbody)
        elif type(postbody) != 'str':
            postbody = str(postbody)

        resp = json.loads(postbody)
        if 'resource_id' not in resp:
            return make_response(
                jsonify(SimpleStatusCodeResponseModel(
                    status=400,
                    message='Bad Request: No resource_id found in request'
                )),
                400
            )

        # identify actinia as source
        resourceID = resp['resource_id']
        status = resp['status']

        # TODO: define when to send cloudevent

        if status == 'finished':
            # TODO send cloudevent
            pass

        terminate_status = ['finished', 'error', 'terminated']
        if status in terminate_status:
            # TODO send cloudevent
            pass

        return make_response(jsonify(resourceID, status), 200)
