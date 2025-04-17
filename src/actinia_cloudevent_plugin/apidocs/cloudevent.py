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


from actinia_cloudevent_plugin.model.response_models import (
    SimpleStatusCodeResponseModel,
)


# class ProcessesJobResponseModel(Schema):
#     """Response schema for creating a job"""
#     type = 'object'
#     properties = {
#         'id': {
#             'type': 'integer',
#             'description': 'The job ID'
#         },
#         'time_created': {
#             'type': 'string',
#             'description': 'Timestamp when job was created'
#         },
#         'time_started': {
#             'type': 'string',
#             'description': 'Timestamp when job was created'
#         },
#         'time_estimated': {
#             'type': 'string',
#             'description': 'Timestamp when job was created'
#         },
#         'time_ended': {
#             'type': 'string',
#             'description': 'Timestamp when job was created'
#         },
#         'status': {
#             'type': 'string',
#             'description': 'Status of the Job',
#             'enum': [
#                 "PENDING",
#                 "RUNNING",
#                 "SUCCESS",
#                 "ERROR",
#                 "TERMINATED"
#             ]
#         },
#         'resource_response': {
#             'type': 'object',
#             'description': 'The Response at creation time'
#         },
#         'resource_id': {
#             'type': 'string',
#             'description': 'The resource ID for the job'
#         },
#         'creation_uuid': {
#             'type': 'string',
#             'description': 'A unique id for the job at creation time before '
#                            'id is known. (More unique than creation '
#                            'timestamp)'
#         }
#     }
#     example = jobs_get_docs_response_example

# describe_ld_get_docs = {
#     # "summary" is taken from the description of the get method
#     "tags": ["example"],
#     "description": "Hello World example",
#     "responses": {
#         "200": {
#             "description": "This response returns the string 'Hello World!'",
#             "schema": SimpleStatusCodeResponseModel,
#         },
#     },
# }

describe_cloudevent_post_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["cloudevent"],
    "description": "Receives dloudevent, transforms to PC and returns cloudevent.",
    "responses": {
        "200": {
            "description": "TODO",
            "schema": SimpleStatusCodeResponseModel,
        },
        # "400": {
        #     "description": "This response returns a detail error message",
        #     "schema": {
        #         "type": "object",
        #         "properties": {
        #             "message": {
        #                 "type": "string",
        #                 "description": "detailed message",
        #                 "example": "Missing name in JSON content",
        #             },
        #         },
        #     },
        # },
    },
}
