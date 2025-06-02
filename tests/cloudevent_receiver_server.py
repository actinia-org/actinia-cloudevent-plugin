# used from sdk-python
# -> https://github.com/cloudevents/sdk-python/blob/main/samples/http-json-cloudevents/json_sample_server.py

from flask import Flask, request

from cloudevents.http import from_http

app = Flask(__name__)


@app.route("/", methods=["POST"])
def home():
    # create a CloudEvent
    event = from_http(request.headers, request.get_data())

    # you can access cloudevent fields as seen below
    print(
        f"Found {event['id']} from {event['source']} with type "
        f"{event['type']} and specversion {event['specversion']}"
    )

    return "", 204


if __name__ == "__main__":
    app.run(port=3000)
