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
"""

__license__ = "GPLv3"
__author__ = "Lina Krisztian"
__copyright__ = "Copyright 2025 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


import json

import pytest
from flask import Response

from tests.testsuite import TestCase

cloudevent_json = {
    "id": "e3525c6d-bbd8-404d-9fa3-1e421dc99c11",
    "specversion": "1.0",
    "source": "/apps/ui",
    "type": "com.mundialis.actinia.process.send",
    "time": "2025-03-28T10:28:48Z",
    "subject" : "myid",
    "actiniaproject":"nc_spm_08",
    "actiniaqueuename":"",
    "datacontenttype": "application/json",
    "data": {
        "list": [
            {
                "module": "r.slope.aspect",
                "inputs": [
                    {"param": "elevation", "value": "elev_ned_30m@PERMANENT"},
                ],
            },
        ],
    },
}


class CloudeventTest(TestCase):
    """Cloudevent test class for / endpoint."""

    @pytest.mark.integrationtest
    def test_post_cloudevent(self) -> None:
        """Test the post method of the / endpoint."""
        # Expected outcome
        # (Note: returned cloudevent id, changes for each request)
        # Lenght of response
        resp_length = 152
        # Start of response (and according string index)
        resp_start = (
            "Received event e3525c6d-bbd8-404d-9fa3-1e421dc99c11"
            " and returned event "
        )
        resp_start_ind = 71
        # End of response (and according string index)
        resp_end = "with actinia-job <queue_name>_<resource_id>."
        resp_end_ind = 108

        # Test post method
        resp = self.app.post(
            "/",
            data=json.dumps(cloudevent_json),
            content_type="application/json",
        )
        assert isinstance(
            resp,
            Response,
        ), "The response is not of type Response"
        assert resp.status_code == 200, "The status code is not 200"
        assert hasattr(resp, "json"), "The response has no attribute 'json'"
        assert (
            "message" in resp.json
        ), "There is no 'message' inside the response"
        assert len(resp.json["message"]) == resp_length, (
            "The length of response message is wrong. "
            f"{len(resp.json['message'])}, instead of {resp_length}."
        )
        assert resp.json["message"][:resp_start_ind] == resp_start, (
            "The start of response message is wrong. "
            f"'{resp.json['message'][:resp_start_ind]}', "
            f"instead of '{resp_start}'."
        )
        assert resp.json["message"][resp_end_ind:] == resp_end, (
            "The end of response message is wrong. "
            f"'{resp.json['message'][resp_end_ind:]}', "
            f"instead of '{resp_end}'."
        )

    @pytest.mark.integrationtest
    def test_get_cloudevent(self) -> None:
        """Test the get method of the / endpoint."""
        resp = self.app.get("/")
        assert isinstance(
            resp,
            Response,
        ), "The response is not of type Response"
        assert (
            resp.status_code == 405
        ), f"The status code is not 405 but {resp.status_code}."
        assert hasattr(resp, "json"), "The response has no attribute 'json'"
        assert (
            "message" in resp.json
        ), "There is no 'message' inside the response"
        assert resp.json["message"] == "Method Not Allowed", (
            f"The response is wrong. '{resp.json['message']}',"
            "instead of 'Method Not Allowed'"
        )
