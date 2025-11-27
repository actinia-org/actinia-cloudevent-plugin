#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2025 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: GPL-3.0-or-later

Hello World class
"""

__license__ = "GPLv3"
__author__ = "Lina Krisztian"
__copyright__ = "Copyright 2025 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from actinia_cloudevent_plugin.model.response_models import (
    SimpleStatusCodeResponseModel,
)

describe_cloudevent_post_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["cloudevent"],
    "description": (
        "Receives cloudevent, transforms and starts pc and returns cloudevent."
    ),
    "responses": {
        "200": {
            "description": (
                "This response returns received, and returned events, "
                "generated queue name and the status"
            ),
            "schema": SimpleStatusCodeResponseModel,
        },
        "400": {
            "description": "This response returns an error message",
            "schema": SimpleStatusCodeResponseModel,
        },
    },
}
