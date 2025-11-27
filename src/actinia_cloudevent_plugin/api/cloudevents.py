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
__author__ = "Lina Krisztian"
__copyright__ = "Copyright 2025 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"

from flask import jsonify, make_response
from flask_restful_swagger_2 import Resource, swagger
from requests.exceptions import ConnectionError  # noqa: A004

from actinia_cloudevent_plugin.apidocs import cloudevent
from actinia_cloudevent_plugin.core.cloudevents import (
    receive_cloud_event,
    send_binary_cloud_event,
    # send_structured_cloud_event,
    start_actinia_job,
)
from actinia_cloudevent_plugin.model.response_models import (
    SimpleStatusCodeResponseModel,
)
from actinia_cloudevent_plugin.resources.config import EVENTRECEIVER


class Cloudevent(Resource):
    """Cloudevent handling."""

    def __init__(self) -> None:
        """Cloudevent class initialisation."""
        self.msg = (
            "Received event <EVENT1> and returned event <EVENT2>"
            " with actinia-job <ACTINIA_JOB>."
        )

    def get(self):
        """Cloudevent get method: not allowed response."""
        res = jsonify(
            SimpleStatusCodeResponseModel(
                status=405,
                message="Method Not Allowed",
            ),
        )
        return make_response(res, 405)

    @swagger.doc(cloudevent.describe_cloudevent_post_docs)
    def post(self) -> SimpleStatusCodeResponseModel:
        """Cloudevent post method with cloudevent from postbody.

        Receives cloudevent, transforms to process chain (pc),
        sends pc to actinia + start process,
        and returns cloudevent with queue name.
        """
        # Transform postbody to cloudevent
        event_received = receive_cloud_event()
        # With received process chain start actinia process + return cloudevent
        actinia_resp = start_actinia_job(event_received)
        queue_name = actinia_resp["queue"]

        try:
            # TODO: Send event to JobSink
            # TODO: Configure JobSink URL
            # url = TODO
            # new_event = send_binary_cloud_event(
            #     event_received,
            #     queue_name,
            #     url,
            # )

            # Send event to configured broker
            # TODO: binary or structured cloud event?
            url = EVENTRECEIVER.url
            new_event = send_binary_cloud_event(
                event_received,
                actinia_resp["queue"],
                url,
            )
            return SimpleStatusCodeResponseModel(
                status=204,
                message=self.msg.replace("<EVENT1>", event_received["id"])
                .replace("<EVENT2>", new_event["id"])
                .replace("<ACTINIA_JOB>", queue_name),
            )
        except ConnectionError as e:
            return f"Connection ERROR when returning cloudevent: {e}"
