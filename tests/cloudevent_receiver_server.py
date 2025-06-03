#!/usr/bin/env python
"""Helper script for generation server, which receives cloudevents."""
# used from sdk-python
# -> https://github.com/cloudevents/sdk-python/blob/main/samples/http-json-cloudevents/json_sample_server.py

from cloudevents.http import from_http
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def home():
    """Server for cloudevent receival."""
    # create a CloudEvent
    event = from_http(request.headers, request.get_data())

    # you can access cloudevent fields as seen below
    print(
        f"Found {event['id']} from {event['source']} with type "
        f"{event['type']} and specversion {event['specversion']}",
    )

    return "", 204


if __name__ == "__main__":
    app.run(port=3000)
