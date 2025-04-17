#!/usr/bin/env python
"""Copyright (c) 2018-2024 mundialis GmbH & Co. KG.

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
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
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
        # self.msg = "Hello world!"

    # @swagger.doc(helloworld.describe_hello_world_get_docs)
    # def get(self) -> SimpleStatusCodeResponseModel:
    #     """Get 'Hello world!' as answer string."""
    #     return SimpleStatusCodeResponseModel(status=200, message=self.msg)

    @swagger.doc(cloudevent.describe_cloudevent_post_docs)
    def post(self) -> SimpleStatusCodeResponseModel:
        """Cloudevent post method with name from postbody."""
        event = receive_cloud_event()
        queue_name = cloud_event_to_process_chain(event)
        # TODO: binary or structured cloud event?
        send_binary_cloud_event(queue_name)

        return SimpleStatusCodeResponseModel(status=200)
