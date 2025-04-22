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


from flask import make_response, request
from flask_restful_swagger_2 import Resource, swagger

from actinia_cloudevent_plugin.apidocs import cloudevent
from actinia_cloudevent_plugin.core.processing import receive_cloud_event, cloud_event_to_process_chain, send_binary_cloud_event #, send_structured_cloud_event
from actinia_cloudevent_plugin.model.response_models import (
    SimpleStatusCodeResponseModel,
)


class Cloudevent(Resource):
    """Receives cloudevent, transorms to process chain,
    and returns cloudevent with queue name"""

    def __init__(self) -> None:
        """Cloudevent class initialisation."""
        self.msg = "Received event <EVENT1> and returned event <EVENT2> with queue <QUEUE>."

    @swagger.doc(cloudevent.describe_cloudevent_post_docs)
    def post(self) -> SimpleStatusCodeResponseModel:
        """Cloudevent post method with cloudevent from postbody."""
        # Transform postbody to cloudevent
        event_received = receive_cloud_event()
        # Received process chain to queue name
        queue_name = cloud_event_to_process_chain(event_received)
        # TODO: binary or structured cloud event?
        event_returned = send_binary_cloud_event(event_received, queue_name, event_received["cloudeventreceiver"])
        return SimpleStatusCodeResponseModel(status=204, message=self.msg.replace("<EVENT1>",event_received["id"]).replace("<EVENT2>", event_returned["id"]).replace("<QUEUE>" ,queue_name))

