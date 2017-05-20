from stem.util import term
import stem.util.connection, stem.util.system, stem.connection, stem.process, stem.control
import colorama, socket, socks

colorama.init(autoreset=True)


pids = lambda: stem.util.system.pid_by_name("tor", multiple = True)
resolvers = stem.util.connection.system_resolvers()
connections = lambda pid=None, resolver=None: stem.util.connection.get_connections(resolver if resolver else self.resolvers[0], process_pid = pid if pid else self.pids()[0], process_name = "tor") if self.resolvers and self.pids else None

def proxify(address: str = "127.0.0.1", port: int = 9150):
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, address, port)
    socket.socket = socks.socksocket
    def getaddrinfo(*args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (args[0], args[1]))]
    socket.getaddrinfo = getaddrinfo

class SockSocket(socks.socksocket):
    def __init__(self, family: socket.AddressFamily = socket.AddressFamily.AF_INET, type: socket.SocketKind = socket.SocketKind.SOCK_STREAM, proto: int = 0, address: str = "127.0.0.1", port: int = 9150, *args, **kwargs):
        super(SockSocket, self).__init__(family, type, proto, *args, **kwargs)
        self.set_proxy(socks.PROXY_TYPE_SOCKS5, address, port)
        self.address = address
        self.port = port
    
    def getaddrinfo(self, *args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (args[0], args[1]))]

class Controller(stem.control.Controller):
    def __init__(self, address: str = "127.0.0.1", port: int = "default", password: str = None, chroot_path: str = None, protocolinfo_response=None):
        if not stem.util.connection.is_valid_ipv4_address(address):
            raise ValueError("Invalid IP address: %s" % address)
        elif port != "default" and not stem.util.connection.is_valid_port(port):
            raise ValueError("Invalid port: %s" % port)
        
        if port == "default":
            control_port = stem.connection._connection_for_default_port(address)
        else:
            control_port = stem.socket.ControlPort(address, port)
        super(Controller, self).__init__(control_port)
        self.authenticate(password=password, chroot_path=chroot_path, protocolinfo_response=protocolinfo_response)

class Tor(object):
    def __init__(self):
        self.process = None
        self.config = {"SocksPort": 9150, "ControlPort": 9151}
    
    def _handle_line(self, line):
        if "Bootstrapped" in line:
            print(line)
    
    def start(self, quiet: bool = True, msg_prefix: str = "", msg_color: str = "yellow", **config):
        """Start this Tor instance and a new tor process ...
           Argumments:
           - quiet: If True, print bootstrap lines.
           - **config: Config to pass to the process at its initialization."""
        if not self.process:
            for key, value in self.config.items():
                if key not in config:
                    config[key] = str(value)
            self.process = stem.process.launch_tor_with_config(config = config, init_msg_handler = None if quiet else lambda line: self._handle_line(term.format(f"{msg_prefix}{line}", msg_color)))
            self.config = config
    
    def exit(self):
        """Kill this Tor process only if it already have successfully started, otherwise, pass."""
        if self.process:
            self.process.kill()

class HiddenService(object):
    def __init__(self, address, controller: Controller = None):
        if not controller:
            self.controller = Controller()
        
        self.address = (address + ".onion" if len(address) == 16 else address).lower()
        self.descriptor = self.controller.get_hidden_service_descriptor(address)
        self.introduction_points = self.descriptor.introduction_points
        for key in self.descriptor.ATTRIBUTES:
            setattr(self, key, getattr(self.descriptor, key))
