#!/usr/bin/env python
"""Copyright (c) 2025 mundialis GmbH & Co. KG.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Logging interface
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2025, mundialis"
__maintainer__ = ""


import logging
from datetime import datetime, timezone
from logging import FileHandler

from colorlog import ColoredFormatter
from pythonjsonlogger import jsonlogger

from actinia_cloudevent_plugin.resources.config import LOGCONFIG

# Notice: do not call logging.warning (will create new logger for ever)
# logging.warning("called actinia_cloudevent_plugin logger after 1")

log = logging.getLogger("actinia-cloudevent-plugin")
werkzeugLog = logging.getLogger("werkzeug")
gunicornLog = logging.getLogger("gunicorn")


def setLogFormat(veto=None):
    """Set format of logs."""
    logformat = ""
    if LOGCONFIG.type == "json" and not veto:
        logformat = CustomJsonFormatter(
            "%(time) %(level) %(component)"
            "%(module) %(message) %(pathname)"
            "%(lineno) %(processName)"
            "%(threadName)",
        )
    else:
        logformat = ColoredFormatter(
            "%(log_color)s[%(asctime)s] %(levelname)-10s: %(name)s.%(module)-"
            "10s -%(message)s [in %(pathname)s:%(lineno)d]%(reset)s",
        )
    return logformat


def setLogHandler(logger, logtype, logformat) -> None:
    """Set handling of logs."""
    if logtype == "stdout":
        handler = logging.StreamHandler()
    elif logtype == "file":
        # For readability, json is never written to file
        handler = FileHandler(LOGCONFIG.logfile)
    handler.setFormatter(logformat)
    logger.addHandler(handler)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Customized formatting of logs as json."""

    def add_fields(self, log_record, record, message_dict) -> None:
        """Add fiels for json log."""
        super(CustomJsonFormatter, self).add_fields(  # noqa: UP008
            log_record,
            record,
            message_dict,
        )

        # (Pdb) dir(record)
        # ... 'args', 'created', 'exc_info', 'exc_text', 'filename', 'funcName'
        # ,'getMessage', 'levelname', 'levelno', 'lineno', 'message', 'module',
        # 'msecs', 'msg', 'name', 'pathname', 'process', 'processName',
        # 'relativeCreated', 'stack_info', 'thread', 'threadName']
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        log_record["time"] = now
        log_record["level"] = record.levelname
        log_record["component"] = record.name


def createLogger() -> None:
    """Create logger, set level and define format."""
    log.setLevel(getattr(logging, LOGCONFIG.level))
    fileformat = setLogFormat("veto")
    stdoutformat = setLogFormat()
    setLogHandler(log, "file", fileformat)
    setLogHandler(log, "stdout", stdoutformat)


def createWerkzeugLogger() -> None:
    """Create werkzeug-logger, set level and define format."""
    werkzeugLog.setLevel(getattr(logging, LOGCONFIG.level))
    fileformat = setLogFormat("veto")
    stdoutformat = setLogFormat()
    setLogHandler(werkzeugLog, "file", fileformat)
    setLogHandler(werkzeugLog, "stdout", stdoutformat)


def createGunicornLogger() -> None:
    """Create gunicorn-logger, set level and define format."""
    gunicornLog.setLevel(getattr(logging, LOGCONFIG.level))
    fileformat = setLogFormat("veto")
    stdoutformat = setLogFormat()
    setLogHandler(gunicornLog, "file", fileformat)
    setLogHandler(gunicornLog, "stdout", stdoutformat)
    # gunicorn already has a lot of children logger, e.g gunicorn.http,
    # gunicorn.access. These lines deactivate their default handlers.
    # pylint: disable=E1101
    for name in logging.root.manager.loggerDict:
        if "gunicorn." in name:
            logging.getLogger(name).propagate = True
            logging.getLogger(name).handlers = []


createLogger()
createWerkzeugLogger()
createGunicornLogger()
