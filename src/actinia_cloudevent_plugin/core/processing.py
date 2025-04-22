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

Example core functionality
"""

__license__ = "GPLv3"
__author__ = "Lina Krisztian"
__copyright__ = "Copyright 2025 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from flask import request
import requests

from cloudevents.http import from_http
from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent


def receive_cloud_event():
    """Return cloudevent from postpody
    """
    # Parses CloudEvent `data` and `headers` into a CloudEvent`.
    event = from_http(request.headers, request.get_data())

    # TODO
    # Process the event (example)
    event_type = event["type"]
    if event_type == "com.example.object.created":
        print("Object created event received!")

    return event


def cloud_event_to_process_chain(event):
    """Return queue name for process chain of event
    """
    
    pc = event.get_data()["list"][0]
    # !! TODO !!: pc to queue
    # NOTE: as core plugin AND/OR as standalone app -> consider for queue name creation
    queue_name="test_queue_name"

    return queue_name
def send_binary_cloud_event(event, queue_name, url):
    """Return posted binary event with queue name
    """
    # TODO: define/configure source + type
    attributes = {
        "specversion": event["specversion"],
        "source" : "/actinia-cloudevent-plugin",
        "type": "TODO",
        "subject": event["subject"],
        "datacontenttype": "application/json",
    }
    data = {"queue": queue_name }

    event = CloudEvent(attributes, data)
    headers, body = to_binary(event)
    # send event
    requests.post(url, headers=headers, data=body)

    return event


def send_structured_cloud_event(event, queue_name, url):
    """Return posted structured event with queue name
    """
    # TODO: define/configure source + type
    attributes = {
        "specversion": event["specversion"],
        "source" : "/actinia-cloudevent-plugin",
        "type": "TODO",
        "subject": event["subject"],
        "datacontenttype": "application/json",
    }
    data = {"queue": queue_name }

    event = CloudEvent(attributes, data)
    headers, body = to_structured(event)
    # send event
    requests.post(url, headers=headers, data=body)

    return event
