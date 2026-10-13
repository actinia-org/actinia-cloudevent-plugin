#!/usr/bin/env python
"""Helper script for generation server, which receives cloudevents.

SPDX-FileCopyrightText: (c) 2025 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

code used from sdk-python
-> https://github.com/cloudevents/sdk-python/blob/main/samples/http-json-cloudevents/json_sample_server.py
"""

from cloudevents.core.bindings.http import HTTPMessage, from_http_event
from cloudevents.core.exceptions import MissingRequiredAttributeError
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def home():
    """Server for cloudevent receival."""
    # create a CloudEvent
    try:
        message = HTTPMessage(headers=request.headers, body=request.get_data())
        event = from_http_event(message)
    except MissingRequiredAttributeError as e:
        return f"ERROR parsing cloudevent: {e}", 400

    # you can access cloudevent fields as seen below
    print(
        f"Found {event.get_id()} from {event.get_source()} with type "
        f"{event.get_type()} and specversion {event.get_specversion()}",
    )

    return "", 204


if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0")
