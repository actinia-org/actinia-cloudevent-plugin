FROM alpine:3.22

# python3 + pip3
# hadolint ignore=DL3018
RUN apk update; \
    apk add --no-cache python3 python3-dev make
ENV PATH="/opt/venv/bin:$PATH"
RUN /usr/bin/python -m venv --system-site-packages --without-pip /opt/venv
# hadolint ignore=DL3013
RUN python -m ensurepip && pip3 install --no-cache-dir --upgrade pip pep517 wheel

# hadolint ignore=DL3013
RUN pip3 install --no-cache-dir gunicorn && \
    # needed for tests
    pip3 install --no-cache-dir setuptools pwgen==0.8.2.post0 pytest==8.3.5 pytest-cov==6.0.0

COPY . /src/actinia-cloudevent-plugin/
RUN pip3 install --no-cache-dir -e /src/actinia-cloudevent-plugin/ && \
    # For tests:
    chmod a+x /src/actinia-cloudevent-plugin/tests_with_cloudevent_receiver.sh

WORKDIR /src/actinia-cloudevent-plugin
# RUN make test

CMD ["gunicorn", "-b", "0.0.0.0:8088", "-w", "8", "--access-logfile=-", "-k", "gthread", "actinia_cloudevent_plugin.main:flask_app"]
