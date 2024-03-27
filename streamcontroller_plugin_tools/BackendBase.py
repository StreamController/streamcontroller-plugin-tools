import argparse
import threading
import sys
from loguru import logger as log

log.remove(0)
log.add(sys.stderr, level="TRACE")

import rpyc
from rpyc.utils.server import ThreadedServer
from rpyc.core.protocol import Connection
import argparse

class BackendBase(rpyc.Service):
    def __init__(self):
        self.frontend_connection: Connection = None
        self.frontend = None
        self.server: ThreadedServer = None

        self.connect_to_frontend()
        self.start_server()
        self.register_to_frontend()

    def connect_to_frontend(self):
        port = self.get_args().port
        self.frontend_connection = rpyc.connect("localhost", port)
        self.frontend = self.frontend_connection.root

    def start_server(self):
        self.server = ThreadedServer(self, port=0, protocol_config={"allow_public_attrs": True})
        # self.server.start()
        threading.Thread(target=self.server.start, name="server_start", daemon=False).start()
        log.success("Started server")

    def register_to_frontend(self):
        self.frontend.register_backend(port=self.server.port)

    def on_disconnect(self, conn):
        log.info("Connection closed")
        if self.server is not None:
            self.server.close()
        if self.frontend_connection is not None:
            self.frontend_connection.close()

    def get_args(self):
        parser = argparse.ArgumentParser(prog="BackendBase")
        parser.add_argument("--port", type=str)
        args = parser.parse_args()
        if args.port is None:
            parser.print_help()
            sys.exit()
        return args