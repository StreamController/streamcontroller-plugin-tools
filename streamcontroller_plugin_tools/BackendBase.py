import argparse
import Pyro5.api
import threading
import time
import sys
import os
from loguru import logger as log

log.add(sys.stderr, level="TRACE")

@Pyro5.api.expose
class BackendBase:
    def __init__(self):
        self.daemon:Pyro5.api.Daemon = None
        self.init_pyro5()

        self._frontend:Pyro5.api.Proxy = None
        self.connect_to_frontend()
        self.register_to_frontend()

        threading.Thread(target=self.ping_thread, daemon=True).start()

        self.daemon.requestLoop()

    def connect_to_frontend(self):
        args = self.get_args()
        log.info(f"Connecting to {args.uri}")
        self.frontend = Pyro5.api.Proxy(args.uri)

    def register_to_frontend(self):
        uri = self.daemon.register(self)
        self.frontend.register_backend(backend_uri=uri)

    def init_pyro5(self):
        self.daemon = Pyro5.api.Daemon()
        # threading.Thread(target=self.daemon.requestLoop, daemon=True).start()

    def get_args(self):
        parser = argparse.ArgumentParser(prog="BackendBase")
        parser.add_argument("--uri", type=str)
        args = parser.parse_args()
        if args.uri is None:
            parser.print_help()
            exit()
        return args
    
    @property
    def frontend(self):
        # Transfer ownership
        if self._frontend is not None:
            self._frontend._pyroClaimOwnership()
        return self._frontend

    @frontend.setter
    def frontend(self, value):
        self._frontend = value
    
    def ping_thread(self):
        while True:
            time.sleep(5)
            try:
                self.frontend.ping()
                log.trace("Pinged frontend")
            except Pyro5.errors.ConnectionClosedError:
                log.error("Failed to ping frontend")
                self.on_connection_lost()
                return

    def on_connection_lost(self):
        log.info("on_connection_lost triggered")
        self.daemon.close()
        sys.exit(0)