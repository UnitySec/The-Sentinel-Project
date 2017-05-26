import urllib.parse, requests, bs4
from queue import Queue
from modules.utils import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


__all__ = ["Session"]
__doc__ = "Single class module to simplify common HTTP(s) tasks (such as proxifying, getting and parsing responses, etc)."

class Session(object):
    def __init__(self, url):
        self.session = requests.Session()
        self.session.headers["user-agent"] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
        
        self.request = lambda method, path = "", **kwargs: self.session.request(method, urllib.parse.urljoin(self.base_url.geturl(), path), **kwargs)
        self._request = self.request
        
        self.proxies = Queue()
        
        self.parse = lambda code, module: bs4.BeautifulSoup(code, module)
        self.parse_xml = lambda code: self.parse(code, "lxml")
        self.parse_html = lambda code: self.parse(code, "html.parser")
        
        self.base_url = urllib.parse.urlparse(url)
    
    def load_proxies(self, filename, delimiter="\n"):
        getIP = lambda proxy: requests.get("https://httpbin.org/ip", proxies={"http": proxy, "https": proxy}).json()["origin"]
        myip = getIP("")
        for proxy in readFile(filename, "r").split(delimiter):
            """try:
                ip = getIP(proxy)
                if ip != myip:
                    self.proxies.put(proxy)
            except:
                pass"""
            self.proxies.put(proxy)
    
    def install_proxy(self):
        if self.proxies:
            proxy = self.proxies.get()
            self.session.proxies.update({"http": proxy, "https": proxy})
            self.proxies.task_done()
