#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2025 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: GPL-3.0-or-later

Example core functionality
"""

__license__ = "GPLv3"
__author__ = "Lina Krisztian"
__copyright__ = "Copyright 2025 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


import json

import requests
from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent, from_http
from flask import request
from requests.auth import HTTPBasicAuth

from actinia_cloudevent_plugin.resources.config import ACTINIA, EVENTRECEIVER


def receive_cloud_event():
    """Return cloudevent from postpody."""
    # Parses CloudEvent 'data' and 'headers' into a CloudEvent.
    event = from_http(request.headers, request.get_data())

    # ? TODO
    # eventually Filter the event (see example below)
    event_type = event["type"]
    if event_type == "com.example.object.created":
        print("Object created event received!")

    return event


def start_actinia_job(event) -> str:
    """Return actinia response for process chain of event."""
    pc = event.get_data()
    # NOTE: as standalone app -> consider for queue name creation

    # TODO: Define ce attribute for possible mapset.
    # Also in actiniaproject divided by "/" or "."?
    project = event.get_attributes().get("actiniaproject")
    mapset = None
    if "." in project:
        project = project.split(".")[0]
        mapset = project.split(".")[1]

    url = f"{ACTINIA.processing_base_url}/projects/{project}/"
    if not mapset:
        # emphemeral processing
        if ACTINIA.use_actinia_modules:
            url += "processing_export"
        else:
            url += "processing_async_export"
    # persistent processing
    elif ACTINIA.use_actinia_modules:
        url += f"mapsets/{mapset}/processing"
    else:
        url += f"mapsets/{mapset}/processing_async/"

    postkwargs = dict()
    postkwargs["headers"] = {"content-type": "application/json; charset=utf-8"}
    postkwargs["auth"] = HTTPBasicAuth(ACTINIA.user, ACTINIA.password)
    postkwargs["data"] = json.dumps(pc)

    resp = requests.post(
        url,
        **postkwargs,
    )

    # Part of resp:
    # 'message' = 'Resource accepted'
    # 'queue' = 'job_queue_resource_id-cddae7bb-b4fa-4249-aec4-2a646946ff36'
    # 'resource_id' = 'resource_id-cddae7bb-b4fa-4249-aec4-2a646946ff36'
    # 'status' = 'accepted'
    # 'urls' = {
    #    'resources': [],
    #    'status':
    #    'http://actinia-dev:8088/api/v3/resources/actinia-gdi/
    #    resource_id-cddae7bb-b4fa-4249-aec4-2a646946ff36'}

    return json.loads(resp.text)


def send_binary_cloud_event(event, queue_name, url):
    """Return posted binary event with actinia_job."""
    return send_cloud_event(
        mode="binary",
        version=event["specversion"],
        cetype="com.mundialis.actinia.process.startworker",
        subject=event["subject"],
        actiniaqueuename=queue_name,
        url=url,
    )


def send_structured_cloud_event(event, actinia_job, url):
    """Return posted structured event with actinia_job."""
    # TODO: adjust to queue name
    return send_cloud_event(
        mode="structured",
        version=event["specversion"],
        cetype="com.mundialis.actinia.process.started",
        subject=event["subject"],
        data={"actinia_job": actinia_job},
        url=url,
    )


def send_cloud_event(
    mode="binary",
    version="1.0",
    cetype="com.mundialis.actinia.process.started",
    subject="nc_spm_08/PERMANENT",
    actiniaqueuename=None,
    data="{}",
    url=None,
):
    """Post event and return it."""
    if url is None:
        url = EVENTRECEIVER.url

    attributes = {
        "specversion": version,
        "source": "/actinia-cloudevent-plugin",
        "type": cetype,
        "subject": subject,
        "datacontenttype": "application/json",
        "actiniaqueuename": actiniaqueuename,
    }

    event = CloudEvent(attributes, data)

    # From https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md#message
    # A "structured-mode message" is one where the entire event (attributes and data)
    # are encoded in the message body, according to a specific event format.
    # A "binary-mode message" is one where the event data is stored in the message body,
    # and event attributes are stored as part of message metadata.
    # Often, binary mode is used when the producer of the CloudEvent wishes to add the
    # CloudEvent's metadata to an existing event without impacting the message's body.
    # In most cases a CloudEvent encoded as a binary-mode message will not break an
    # existing receiver's processing of the event because the message's metadata
    # typically allows for extension attributes.
    # In other words, a binary formatted CloudEvent would work for both
    # a CloudEvents enabled receiver as well as one that is unaware of CloudEvents.
    if mode == "binary":
        headers, body = to_binary(event)
    else:
        headers, body = to_structured(event)

    requests.post(url, headers=headers, data=body)

    return event
