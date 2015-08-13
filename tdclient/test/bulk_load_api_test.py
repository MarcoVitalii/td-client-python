#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals

import io
import msgpack
try:
    from unittest import mock
except ImportError:
    import mock
import pytest
import time

from tdclient import api
from tdclient.test.test_helper import *

def setup_function(function):
    unset_environ()

seed = {
    "config": {
        "in": {
            "type": "s3",
            "access_key_id": "abcdefg",
            "secret_access_key": "hijklmn",
            "bucket": "bucket",
            "path_prefix": "prefix",
        },
        "out": {
            "mode": "append",
        },
    },
}

config = {
    "config": {
        "in": {
            "type": "s3",
            "access_key_id": "abcdefg",
            "secret_access_key": "hijklmn",
            "bucket": "bucket",
            "path_prefix": "prefix",
            "decoders": [
                {"type": "gzip"},
            ],
            "parser": {
                "charset": "UTF-8",
                "newline": "CRLF",
                "delimiter": ",",
                "quote": "",
                "escape": "",
                "skip_header_lines": 1,
                "allow_extra_columns": False,
                "allow_optional_columns": False,
                "columns": [
                    {"name": "member_id", "type": "long"},
                    {"name": "goods_id", "type": "long"},
                    {"name": "category", "type": "string"},
                    {"name": "sub_category", "type": "string"},
                    {"name": "order_date", "type": "timestamp", "format": "%Y-%m-%d %H:%M:%S"},
                    {"name": "ship_date", "type": "timestamp", "format": "%Y-%m-%d"},
                    {"name": "amount", "type": "long"},
                    {"name": "price", "type": "long"},
                ]
            },
        },
        "out": {
            "mode": "append",
        },
    },
}

def test_bulk_load_guess_success():
    td = api.API("APIKEY")
    td.post = mock.MagicMock(return_value=make_response(200, json.dumps(config).encode("utf-8")))
    res = td.bulk_load_guess(seed)
    assert res == config
    td.post.assert_called_with("/v3/bulk_loads/guess", seed)

def test_bulk_load_preview_success():
    td = api.API("APIKEY")
    body = b"{}"
    td.post = mock.MagicMock(return_value=make_response(200, body))
    td.bulk_load_preview(config)
    td.post.assert_called_with("/v3/bulk_loads/preview", config)

def test_bulk_load_issue_success():
    td = api.API("APIKEY")
    body = b"""
      {"job_id": 12345}
    """
    td.post = mock.MagicMock(return_value=make_response(200, body))
    res = td.bulk_load_issue("database", "table", config)
    assert res == "12345"
    req = dict(config)
    req["database"] = "database"
    req["table"] = "table"
    td.post.assert_called_with("/v3/job/issue/bulkload/database", req)

def test_bulk_load_list_success():
    td = api.API("APIKEY")
    body = b"{}"
    td.get = mock.MagicMock(return_value=make_response(200, body))
    td.bulk_load_list()
    td.get.assert_called_with("/v3/bulk_loads")

def test_bulk_load_create_success():
    td = api.API("APIKEY")
    body = b"{}"
    td.post = mock.MagicMock(return_value=make_response(200, body))
    td.bulk_load_create("name", "database", "table", config)
    req = dict(config)
    req["name"] = "name"
    req["database"] = "database"
    req["table"] = "table"
    td.post.assert_called_with("/v3/bulk_loads", req)

def test_bulk_load_show_success():
    td = api.API("APIKEY")
    body = b"{}"
    td.get = mock.MagicMock(return_value=make_response(200, body))
    td.bulk_load_show("name")
    td.get.assert_called_with("/v3/bulk_loads/name")

def test_bulk_load_update_success():
    td = api.API("APIKEY")
    body = b"{}"
    td.put = mock.MagicMock(return_value=make_response(200, body))
    td.bulk_load_update("name", config)
    td.put.assert_called_with("/v3/bulk_loads/name", config)

def test_bulk_load_delete_success():
    td = api.API("APIKEY")
    body = b"{}"
    td.delete = mock.MagicMock(return_value=make_response(200, body))
    td.bulk_load_delete("name")
    td.delete.assert_called_with("/v3/bulk_loads/name")

def test_bulk_load_history_success():
    td = api.API("APIKEY")
    body = b"{}"
    td.get = mock.MagicMock(return_value=make_response(200, body))
    td.bulk_load_history("name")
    td.get.assert_called_with("/v3/bulk_loads/name")

def test_bulk_load_run_success():
    td = api.API("APIKEY")
    body = b"{}"
    td.post = mock.MagicMock(return_value=make_response(200, body))
    td.bulk_load_run("name", scheduled_time="scheduled_time")
    td.post.assert_called_with("/v3/bulk_loads/name", {"scheduled_time": "scheduled_time"})
