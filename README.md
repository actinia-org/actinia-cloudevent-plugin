# actinia-cloudevent-plugin

This is a plugin for [actinia-core](https://github.com/mundialis/actinia_core) which translates cloudevents into a process definition
for actinia-core and runs as standalone app.

## Installation and Setup

Use docker-compose for installation:
```bash
docker compose -f docker/docker-compose.yml build
docker compose -f docker/docker-compose.yml up -d
```

### DEV setup with vscode
1. Start actinia-core locally via local dev-setup as described in the
[actinia-docker repository](https://github.com/actinia-org/actinia-docker#local-dev-setup-for-actinia-core-plugins-with-vscode)
2. Have this repository open locally with vscode and press `F5`.
After a few seconds, a browser window should be openend, pointing to
an endpoint (showing 405 Method Not Allowed as this plugin has only
HTTP POST endpoints so far).

Alternatively, configure actinia-core to run jobs via actinia-worker.
In the actinia-core dev-setup, use the `per_job` queue in
`actinia-docker/actinia-dev/actinia.cfg`:
```
[QUEUE]
# queue_type = local

[QUEUE]
queue_type = per_job
kvdb_queue_server_url = valkey
kvdb_queue_server_password = pass
worker_queue_prefix = job_queue
```
And restart the vscode debugger. This way, a job is registered in the
valkey DB, but not directly started.


<!-- TODO: check update docker-compose DEV setup if needed -->
<!-- ```bash
# Uncomment the volume mount of the cloud-event-plugin within docker/docker-compose.yml,
# then:
docker compose -f docker/docker-compose.yml build
docker compose -f docker/docker-compose.yml run --rm --service-ports --entrypoint sh actinia-cloudevent
# within docker
# install the plugin
pip3 install .
# start flask app with actinia-cloudevent-plugin
gunicorn -b 0.0.0.0:5000 -w 8 --access-logfile=- -k gthread actinia_cloudevent_plugin.main:flask_app
# or directly via python
python3 -m actinia_cloudevent_plugin.main
``` -->

## Configuration

- the URL of actinia-core and the cloudevent receiver is defined
within [config/mount/sample.ini](config/mount/sample.ini): `
[EVENTRECEIVER]` (Default value defined within
[src/actinia_cloudevent_plugin/resources/config.py](src/actinia_cloudevent_plugin/resources/config.py))

## Requesting endpoint
**Note**: Assuming cloudevent-plugin is running as described in previous setup.

You can test the plugin and request the `/` endpoint, e.g. with:
```bash
JSON=tests/examples/cloudevent_example.json
curl -X POST -H 'Content-Type: application/json' --data @$JSON localhost:3003/
```
Or test with `per_job` queue
```bash
JSON=tests/examples/cloudevent_example.json
curl -X POST -H 'Content-Type: application/json' --data @$JSON localhost:3003/
# Get the actinia job queue name from the response
QUEUE_NAME=job_queue_resource_id-d4d9be86-5938-47ff-9c6d-7c79964862c0

docker run --rm --network actinia-docker_actinia-dev \
  -v $HOME/actinia/grassdb:/actinia_core/grassdb \
  -v $HOME/actinia/grassdb_user:/actinia_core/userdata \
  --entrypoint actinia-worker actiniacore -q $QUEUE_NAME
```

Exemplary returned cloudevent: [tests/examples/cloudevent_example_return.json](tests/examples/cloudevent_example_return.json)


## Running tests
You can run the tests in the actinia test docker.
These are the same steps which the github workflow is executing.

```bash
docker compose -f docker/docker-compose.yml up -d --build
sleep 10 && \
    docker logs docker-actinia-cloudevent-1 && echo && \
    docker logs docker-actinia-core-1 && echo && \
    docker logs docker-event-receiver-server-1
docker exec -t docker-actinia-cloudevent-1 make integrationtest
docker compose -f docker/docker-compose.yml down
```

---

## Possible setup

```mermaid
graph

    1[Event Emitter, e.g. UI]
    2[Kafka Queue Broker]
    subgraph actinia
        direction TB
        3[actinia-cloudevent-plugin Transformer Service]
        %%3@{ shape: braces, label: "Transformer Service" }
        4[actinia worker JobSink]
        %%4@{ shape: braces, label: "JobSink" }
        5[actinia-core]
        %%5@{ shape: braces, label: " write job to valkey" }
        6[valkey]
    end

    1 -- Cloudevent --> 2
    2 <-- Cloudevent --> 3
    3 -- 1: func,RDC --> 5
    5 -- 2: func,RDC --> 6
    3 -- 3: Cloudevent (queue Name) per HTTP --> 4
    4 -- 4: func,RDC --> 6
    4 -- 5: webhook --> 3
    3 -- Cloudevent (status) --> 2

```
---

<!-- <script>
  mermaid.initialize({ sequence: { showSequenceNumbers: true } });
</script> -->

```mermaid
sequenceDiagram
    autonumber
    create participant event receiver
    create actor event sender
    create participant A as actinia-cloudevent-plugin<br/>Transformer Service
    %% Note right of A: Transformer Service #9829;
    event sender-->>A: Cloudevent
    create participant D as actinia-core
    A->>D: func,RDC
    create participant V as valkey
    D->>V: func,RDC
    D->>A: return <<QUEUE NAME>>
    create participant W as actinia worker<br/>JobSink
    A-XW: Cloudevent with <<QUEUE NAME>> per HTTP
    A-->>event receiver: new Cloudevent with <<QUEUE NAME>>
    destroy event sender
    A-->>event sender: return "Received event <<ID>><br>and returned event <<ID 2>><br> with actinia-job <<QUEUE NAME>>."
    rect rgb(191, 223, 255)
    W->>V: func,RDC
    par Processing
        loop process
            W->>W:
        end
    and Webhook
    opt Optional
        W->>A: status webhook (running)
        A-->>event receiver: Cloudevent (status)
    end
    end
    destroy W
    W->>A: status webhook (finished / error)
    A-->>event receiver: Cloudevent (status)
    end

```
---
