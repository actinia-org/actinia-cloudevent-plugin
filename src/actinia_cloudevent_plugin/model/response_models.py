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

Response models
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from typing import ClassVar

from flask_restful_swagger_2 import Schema


class SimpleStatusCodeResponseModel(Schema):
    """Simple response schema to inform about status."""

    type: str = "object"
    properties: ClassVar[dict] = {
        "status": {
            "type": "number",
            "description": "The status code of the request.",
        },
        "message": {
            "type": "string",
            "description": "A short message to describes the status",
        },
    }
    required: ClassVar[list[str]] = ["status", "message"]


simple_response_example = SimpleStatusCodeResponseModel(
    status=200,
    message="success",
)
SimpleStatusCodeResponseModel.example = simple_response_example
