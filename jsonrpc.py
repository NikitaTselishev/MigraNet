from typing import *
from json import loads
from logging import Logger, getLogger


_logger: Logger = getLogger(__file__)


VERSION = "2.0"


class JSONRPCError(Exception):
    ...


class UnknownMethodError(JSONRPCError):
    ...


class InvalidJSONRPCEStructureError(JSONRPCError):
    ...


class InvalidJSONError(JSONRPCError):
    ...


class IncorrectParamsError(JSONRPCError):
    ...


class InternalError(JSONRPCError):
    ...


def create_json_response(json: Dict[str, Any], result: Any) -> Dict[str, Any]:
    return {"jsonrpc": VERSION, "id": json["id"], "result": result}


def validate_json(json: Dict[str, Any]) -> None:
    version = json.get("jsonrpc")
    if version is not None:
        keys = json.keys()
        if version == VERSION and "method" in keys and "id" in keys:
            return
    raise InvalidJSONRPCEStructureError(
        {"code": -32600, "message": "Invalid Request"}
    )


class Dispatcher:

    _dispatcher: Dict[str, Dict[str, Any]] = {}
    _methods_names: Set[str] = set()

    @staticmethod
    def register(
        method_name: str, required_params: Optional[List[List[str]]] = None
    ) -> Callable:
        def _inner(f: Callable):
            Dispatcher._dispatcher[method_name] = {
                "function": f,
                "required_params": required_params,
            }
            Dispatcher._methods_names.add(method_name)
            return f

        return _inner

    @staticmethod
    def call(data: Any) -> Any:
        try:
            json = loads(data)
        except Exception as exc:
            _logger.exception(exc)
            raise InvalidJSONError({"code": -32700, "message": "Parse error"})
        validate_json(json)
        if json["method"] not in Dispatcher._methods_names:
            raise UnknownMethodError(
                {"code": -32601, "message": "Method not found"}
            )
        method = Dispatcher._dispatcher[json["method"]]
        required_params = method["required_params"]
        if required_params is not None:
            current_params = json["params"]
            for params_pack in required_params:
                for param in params_pack:
                    if param not in current_params:
                        break
                else:
                    break
            else:
                raise IncorrectParamsError(
                    {"code": -32602, "message": "Invalid params"}
                )
        try:
            return method["function"](json=json)
        except JSONRPCError as exc:
            _logger.exception(exc)
            raise exc
        except Exception as exc:
            _logger.exception(exc)
            raise InternalError({"code": -32603, "message": "Internal error"})
