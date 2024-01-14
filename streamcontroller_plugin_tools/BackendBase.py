import argparse
import Pyro5.api
import threading

@Pyro5.api.expose
class BackendBase:
    def __init__(self):
        self.daemon:Pyro5.api.Daemon = None
        self.init_pyro5()

        self.frontend:Pyro5.api.Proxy = None
        self.connect_to_frontend()
        self.register_to_frontend()

    def connect_to_frontend(self):
        args = self.get_args()
        self.frontend = Pyro5.api.Proxy(args.uri)

    def register_to_frontend(self):
        uri = self.daemon.register(self)
        self.frontend.register_backend(backend_uri=uri)

    def init_pyro5(self):
        self.daemon = Pyro5.api.Daemon()
        threading.Thread(target=self.daemon.requestLoop).start()

    def get_args(self):
        parser = argparse.ArgumentParser(prog="BackendBase")
        parser.add_argument("--uri", type=str)
        args = parser.parse_args()
        if args.uri is None:
            parser.print_help()
            exit()
        return args