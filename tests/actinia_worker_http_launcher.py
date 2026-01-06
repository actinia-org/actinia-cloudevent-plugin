#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2025 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: GPL-3.0-or-later

Endpoint to start an actinia-worker container and pass a queue name
"""

__license__ = "GPL-3.0-or-later"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2025 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from fastapi import FastAPI

from docker import from_env

app = FastAPI()
client = from_env()

"""Hints for development

This http server serves as a mockup for a knative JobSink.
Example to start a job from JobSink is by posting a CloudEvent.

kubectl run curl --image=curlimages/curl --rm=true -ti -- -X POST -v \
   -H "content-type: application/json"  \
   -H "ce-specversion: 1.0" \
   -H "ce-source: my/curl/command" \
   -H "ce-type: org.actinia.queuename" \
   -H "ce-id: 150" \
   -H "ce-actiniaqueuename: job_queue_resource_id-4263d323-829e-4a09-b3f3-6fbbfbd72a67" \
   -d "{"pc":"dummyprocesschain"}" \
   http://job-sink.knative-eventing.svc.cluster.local/processing/actinia-processing-job

The started container has the CloudEvent written to an event file.

{
  "specversion": "1.0",
  "id": "150",
  "source": "my/curl/command",
  "type": "org.actinia.queuename",
  "datacontenttype": "application/json",
  "data": {
    "pc": "dummyprocesschain"
  },
  "actiniaqueuename": "job_queue_resource_id-4263d323-829e-4a09-b3f3-6fbbfbd72a67"
}

The job will parse the queue name and start the worker with a helper script.
This workaround is not needed here, the queue name is not mounted but passed
via HTTP GET parameter.
"""


@app.post("/launch/{queue_name}")
def start_container(queue_name: str):
    """Start actinia-worker and hand over queue name.

    Receive an actinia queue_name and launch an actinia-worker via
    docker to start the worker watching for the queue and process it.

    Args:
        queue_name (str): actinia queue name to pass to the worker

    Returns:
        dict: response including status

    """
    client.containers.run(
        "actiniacore",
        command=f"-q {queue_name}",
        entrypoint="actinia-worker",
        network="actinia-docker_actinia-dev",
        name="actinia-worker",
        auto_remove=True,
        detach=True,
    )

    return {"status": "started actinia-worker container"}
