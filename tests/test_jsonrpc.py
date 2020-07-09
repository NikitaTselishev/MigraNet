from typing import *
from json import loads, dumps
from unittest import TestCase

from jsonrpc import (
    Dispatcher,
    InternalError,
    InvalidJSONError,
    IncorrectParamsError,
    UnknownMethodError,
    InvalidJSONRPCEStructureError,
)


@Dispatcher.register("hello")
def first(json: Dict[str, Any]) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "result": 1, "id": 2}


@Dispatcher.register(
    "hello2", required_params=[["js1", "js2"], ["gs1", "gs2"]]
)
def second(json: Dict[str, Any]) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "result": 2, "id": 3}


@Dispatcher.register("hello3")
def third(json: Dict[str, Any]) -> Dict[str, Any]:
    raise Exception("Boom")


class JSONRPCTests(TestCase):
    def test_first(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "result": 1, "id": 2},
            Dispatcher.call(
                dumps({"jsonrpc": "2.0", "method": "hello", "id": 1})
            ),
        )

    def test_second_normally(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "result": 2, "id": 3},
            Dispatcher.call(
                dumps(
                    {
                        "jsonrpc": "2.0",
                        "method": "hello2",
                        "params": {"js1": 1, "js2": 2},
                        "id": 1,
                    }
                )
            ),
        )
        self.assertEqual(
            {"jsonrpc": "2.0", "result": 2, "id": 3},
            Dispatcher.call(
                dumps(
                    {
                        "jsonrpc": "2.0",
                        "method": "hello2",
                        "params": {"gs1": 1, "gs2": 2},
                        "id": 1,
                    }
                )
            ),
        )
        with self.assertRaises(IncorrectParamsError):
            Dispatcher.call(
                dumps(
                    {
                        "jsonrpc": "2.0",
                        "method": "hello2",
                        "params": {"js1": 1, "gs2": 2},
                        "id": 1,
                    }
                )
            )

    def test_third(self):
        with self.assertRaises(InternalError):
            Dispatcher.call(
                dumps({"jsonrpc": "2.0", "method": "hello3", "id": 1})
            )

    def test_other(self):
        with self.assertRaises(InvalidJSONError):
            Dispatcher.call({"jsonrpc": "2.0", "method": "hello1", "id": 1})
        with self.assertRaises(UnknownMethodError):
            Dispatcher.call(
                dumps({"jsonrpc": "2.0", "method": "hello4", "id": 1})
            )
        with self.assertRaises(InvalidJSONRPCEStructureError):
            Dispatcher.call(dumps({"jsonrpc": "2.0", "method": "hello1"}))
        with self.assertRaises(InvalidJSONRPCEStructureError):
            Dispatcher.call(
                dumps({"jsonrpc": "3.0", "method": "hello1", "id": 1})
            )
        with self.assertRaises(InvalidJSONRPCEStructureError):
            Dispatcher.call(
                dumps({"jsonrpc": "2.0", "meth": "hello1", "id": 1})
            )
