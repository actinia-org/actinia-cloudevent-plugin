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

Example core functionality
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from flask import request
import requests

from cloudevents.http import from_http
from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent


def receive_cloud_event():
    """Return cloudevent fields core function.

    Args:
        inp (str): Input string with cloudevent json

    Returns:
        (str) cloudevent fields

    """
    # Parses CloudEvent `data` and `headers` into a CloudEvent`.
    event = from_http(request.headers, request.get_data())

    return event


def cloud_event_to_process_chain(event):
    # you can access cloudevent fields as seen below
    # print(
    #     f"Found {event['id']} from {event['source']} with type "
    #     f"{event['type']} and specversion {event['specversion']}"
    # )
    
    # TODO
    queue_name="test_queue_name"
    pc = event["data"]["list"]

    return queue_name

def send_binary_cloud_event(queue_name, url):
    # This data defines a binary cloudevent
    # TODO
    attributes = {
        "type": "com.example.sampletype1",
        "source": "https://example.com/event-producer",
    }
    data = {"queue": queue_name }

    event = CloudEvent(attributes, data)
    headers, body = to_binary(event)

    # send and print event
    requests.post(url, headers=headers, data=body)
    print(f"Sent {event['id']} from {event['source']} with {event.data}")


# def send_structured_cloud_event(url):
#     # This data defines a binary cloudevent
#     attributes = {
#         "type": "com.example.sampletype2",
#         "source": "https://example.com/event-producer",
#     }
#     data = {"message": "Hello World!"}

#     event = CloudEvent(attributes, data)
#     headers, body = to_structured(event)

#     # send and print event
#     requests.post(url, headers=headers, data=body)
#     print(f"Sent {event['id']} from {event['source']} with {event.data}")
