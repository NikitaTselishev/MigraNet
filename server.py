import http.server
from typing import *
from json import dumps
from logging import Logger, getLogger

import api
import config
import jsonrpc
import database


_logger: Logger = getLogger(__file__)


def create_json_with_error(exc: jsonrpc.JSONRPCError) -> Dict[str, Any]:
    return {"jsonrpc": jsonrpc.VERSION, "id": None, "error": exc.args[0]}


class JSONRPCHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, json: Dict[str, Any]):
        data = dumps(json).encode(errors="replace")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        content_length = self.headers.get("Content-Length")
        if content_length is None:
            self.send_error(400, "Content-Length expected")
            return
        data = self.rfile.read(int(content_length))
        try:
            self._send_json(jsonrpc.Dispatcher.call(data))
        except jsonrpc.JSONRPCError as exc:
            self._send_json(create_json_with_error(exc))
        except Exception as exc:
            _logger.exception(exc)
            self.send_error(400)


if __name__ == "__main__":
    db = database.Database(
        config.DB_HOST, config.DB_NAME, config.DB_USER, config.DB_PASSWORD
    )
    api.init(db)
    server_address = (config.SERVER_HOST, config.SERVER_PORT)
    httpd = http.server.ThreadingHTTPServer(server_address, JSONRPCHandler)
    httpd.serve_forever()
