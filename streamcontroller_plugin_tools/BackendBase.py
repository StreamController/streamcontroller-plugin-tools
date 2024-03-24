import argparse
import Pyro5.api
import threading
import time
import sys
import os
from loguru import logger as log

log.remove(0)
log.add(sys.stderr, level="TRACE")

@Pyro5.api.expose
class BackendBase:
    def __init__(self):
        self.daemon:Pyro5.api.Daemon = None
        log.trace("Init Pyro...")
        self.init_pyro5()
        log.trace("Pyro init done")

        self._frontend:Pyro5.api.Proxy = None
        self.connect_to_frontend()
        log.trace("Connected to frontend")
        self.register_to_frontend()
        log.trace("Registered to frontend")

        self.ping = True
        threading.Thread(target=self.ping_thread, daemon=True, name="ping_thread").start()
        log.trace("Ping thread started")

        self.loop = True
        self.request_loop_thread = threading.Thread(
            target=self.daemon.requestLoop,
            kwargs={"loopCondition": lambda: self.loop}
        )

        self.request_loop_thread.start()
        log.trace("Request loop thread started")

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
        while self.ping:
            time.sleep(5)
            try:
                self.frontend.ping()
                log.trace("Pinged frontend")
            except Pyro5.errors.ConnectionClosedError:
                log.error("Failed to ping frontend")
                self.on_connection_lost()
                return

    def on_connection_lost(self):
        self.loop = False
        self.ping = False
        log.info("on_connection_lost triggered")
        # join all threads
        self.daemon.shutdown()
        log.trace("shutdown daemon done")
        self.daemon.close()
        log.trace("close daemon done")
        # for t in threading.enumerate():
            # if t is not threading.current_thread():
                # t.join()
        log.success("Backend stopped. Have a nice day!")
        sys.exit(0)