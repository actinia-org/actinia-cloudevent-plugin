# actinia-cloudevent-plugin

This is an plugin for [actinia-core](https://github.com/mundialis/actinia_core) which adds cloudevent endpoints to actinia-core.

You can run actinia-cloudevent-plugin as an actinia-core plugin or as standalone app.

## As standalone app
### With docker
TODO

### Without docker - TODO: remove
#### Requirements
```
sudo apt install \
    python3-venv\
    python3\
```
#### Installation
For local developments outside of docker, it is preferred to run actinia-cloudevent-plugin in a virtual python environment.

Clone repository, create virtual environment and activate it, and install actinia-cloudevent-plugin:
```bash
git clone git@github.com:mundialis/actinia-cloudevent-plugin.git
cd actinia-cloudevent-plugin
virtualenv -p python3 venv
. venv/bin/activate
pip3 install .
```
Run tests:
```
python3 -m pytest
```
Run the server for development:
```bash
python3 -m actinia_cloudevent_plugin.main
```
Or for production use actinia_gdi.wsgi as WSGI callable:
```bash
gunicorn -b :5000 -w 1 --access-logfile=- -k gthread actinia_cloudevent_plugin.wsgi
```
If all done, leave environment
```
deactivate
```

## As actinia-core plugin
### Installation with docker
Use docker-compose for installation:
```bash
docker compose -f docker/docker-compose-plugin.yml build
docker compose -f docker/docker-compose-plugin.yml up -d
```

### Installation hints
* If you get an error like: `ERROR: for docker_kvdb_1  Cannot start service valkey: network xxx not found` you can try the following:
```bash
docker compose -f docker/docker-compose-plugin.yml down
# remove all custom networks not used by a container
docker network prune
docker compose -f docker/docker-compose-plugin.yml up -d
```

### Requesting helloworld endpoint
You can test the plugin and request the `/helloworld` endpoint, e.g. with:
```bash
curl -u actinia-gdi:actinia-gdi -X GET http://localhost:8088/api/v3/helloworld | jq

curl -u actinia-gdi:actinia-gdi -H 'accept: application/json' -H 'Content-Type: application/json' -X POST http://localhost:8088/api/v3/helloworld -d '{"name": "test"}' | jq
```

## DEV setup - as actinia-core plugin
For a DEV setup you can use the docker/docker-compose-plugin.yml:
```bash
docker compose -f docker/docker-compose-plugin.yml build
docker compose -f docker/docker-compose-plugin.yml run --rm --service-ports --entrypoint sh actinia
# OR with mounted source code
docker compose -f docker/docker-compose-plugin.yml run --volume `pwd`:/src/actinia_cloudevent-plugin/  --rm --service-ports --entrypoint sh actinia

# install the plugin
(cd /src/actinia-cloudevent-plugin && python3 setup.py install)
# start actinia-core with your plugin
sh /src/start.sh
# gunicorn -b 0.0.0.0:8088 -w 1 --access-logfile=- -k gthread actinia_core.main:flask_app
```

### Hints

* If you have no `.git` folder in the plugin folder, you need to set the
`SETUPTOOLS_SCM_PRETEND_VERSION` before installing the plugin:
```bash
export SETUPTOOLS_SCM_PRETEND_VERSION=0.0
```
Otherwise you will get an error like this
`LookupError: setuptools-scm was unable to detect version for '/src/actinia-cloudevent-plugin'.`.

* If you make changes in code and nothing changes you can try to uninstall the plugin:
```bash
pip3 uninstall actinia-cloudevent-plugin.wsgi -y
rm -rf /usr/lib/python3.8/site-packages/actinia_cloudevent_plugin.wsgi-*.egg
```

### Running tests
You can run the tests in the actinia test docker:

```bash
docker build -f docker/actinia-cloudevent-plugin-test/Dockerfile -t actinia-cloudevent-plugin-test .
docker run -it actinia-cloudevent-plugin-test -i

cd /src/actinia-cloudevent-plugin/

# run all tests
make test

# run only unittests
make unittest
# run only integrationtests
make integrationtest

# run only tests which are marked for development with the decorator '@pytest.mark.dev'
make devtest
```

## Hint for the development of actinia plugins

### skip permission check
The parameter [`skip_permission_check`](https://github.com/mundialis/actinia_core/blob/main/src/actinia_core/processing/actinia_processing/ephemeral_processing.py#L1420-L1422) (see [example in actinia-statistic plugin](https://github.com/mundialis/actinia_statistic_plugin/blob/master/src/actinia_statistic_plugin/vector_sampling.py#L207))
should only be set to `True` if you are sure that you really don't want to check the permissions.

The skip of the permission check leads to a skipping of:
* [the module check](https://github.com/mundialis/actinia_core/blob/main/src/actinia_core/processing/actinia_processing/ephemeral_processing.py#L579-L589)
* [the limit of the number of processes](https://github.com/mundialis/actinia_core/blob/main/src/actinia_core/processing/actinia_processing/ephemeral_processing.py#L566-L570)
* the limit of the processing time

Not skipped are:
* the limit of the cells
* the mapset/project limitations of the user
