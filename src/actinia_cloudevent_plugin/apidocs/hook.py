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

Apidocs for webhook endpoint
"""

__license__ = "GPLv3"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2025 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from actinia_cloudevent_plugin.model.response_models import (
    SimpleStatusCodeResponseModel,
)

describe_hooks_post_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["cloudevent"],
    "description": (
        "Receives webhook with status update e.g. from actinia-core, transforms to cloudevent and sends it to configurable endpoint."
    ),
    "responses": {
        "200": {
            "description": (
                "This response returns a cloud event, "
                "generated from actinia-core status"
            ),
            "schema": SimpleStatusCodeResponseModel,
        },
        "400": {
            "description": "This response returns an error message",
            "schema": SimpleStatusCodeResponseModel,
        },
    },
}
