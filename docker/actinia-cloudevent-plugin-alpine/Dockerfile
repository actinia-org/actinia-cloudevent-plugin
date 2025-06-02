FROM alpine:3.21

# python3 + pip3
# hadolint ignore=DL3018
RUN apk update; \
    apk add --no-cache python3 python3-dev
ENV PATH="/opt/venv/bin:$PATH"
RUN /usr/bin/python -m venv --system-site-packages --without-pip /opt/venv
# hadolint ignore=DL3018
RUN python -m ensurepip && pip3 install --no-cache-dir --upgrade pip pep517 wheel

# gunicorn
# hadolint ignore=DL3018
RUN pip3 install --no-cache-dir gunicorn

COPY . /src/actinia-cloudevent-plugin/

# SETUPTOOLS_SCM_PRETEND_VERSION is only needed if in the plugin folder is no
# .git folder
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0

WORKDIR /src/actinia-cloudevent-plugin
RUN pip3 install --no-cache-dir -e .
