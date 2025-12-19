#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2025 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: GPL-3.0-or-later

Hello World class
"""

__license__ = "GPL-3.0-or-later"
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
from actinia_cloudevent_plugin.resources.config import ACTINIA, EVENTRECEIVER
from actinia_cloudevent_plugin.resources.logging import log


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
        resource_id = actinia_resp["resource_id"]

        try:
            if queue_name == "local":
                # Nothing to do here, the configured actinia-core
                # instance is using a local queue, meaning that the
                # job is processed directly.
                log.info("No need to start actinia-worker")
            else:
                url = f"{ACTINIA.worker_http_launcher_url}/{queue_name}"
                new_event = send_binary_cloud_event(
                    event_received,
                    queue_name,
                    url,
                )

            # Send event to configured broker
            url = EVENTRECEIVER.url
            # TODO: binary or structured cloud event?
            new_event = send_binary_cloud_event(
                event_received,
                actinia_resp["queue"],
                url,
            )
            response = {
                "status": 201,
                "message": self.msg.replace("<EVENT1>", event_received["id"])
                .replace("<EVENT2>", new_event["id"])
                .replace("<ACTINIA_JOB>", queue_name),
                "actinia_queue_name": queue_name,
                "actinia_job": resource_id,
            }
            return make_response(jsonify(response), 201)

        except ConnectionError as e:
            return f"Connection ERROR when returning cloudevent: {e}"
