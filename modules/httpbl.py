import dns.resolver, socket


__doc__ = "Single class module to identify spammers and the spambots they use to scrape addresses from your website."

class DNSbl(object):
    def __init__(self, access_key: str = "vztjisbgwwij"):
        self.access_key = access_key
        self.map = {"suspicious": [1, 3, 5, 7], "harvester": [2, 3, 6, 7], "spammer": [4, 5, 6, 7]}
        self.search_engines = {0: "Unknown", 1: "AltaVista", 2: "Ask", 3: "Baidu",
                               4: "Excite", 5: "Google", 6: "Looksmart", 7: "Lycos",
                               8: "MSN", 9: "Yahoo", 10: "Cuil", 11: "InfoSeek", 12: "Miscellaneous"}
    
    def query(self, host):
        ip = ""
        info = {"ok": False, "found": False, "last-seen-days": 0, "threat-score": 0, "search-engine-id": 0,
                "type": {"search-engine": False,
                         "suspicious": False,
                         "harvester": False,
                         "spammer": False},
                "message": ""}
        try:
            socket.inet_aton(host)
            ip = host
        except:
            try:
                ip = dns.resolver.query(host)
                if ip:
                    ip = ip[0].to_text()
            except Exception as e:
                info["message"] = f"{e}"
        if ip:
            try:
                answer = dns.resolver.query(".".join([self.access_key] + ip.split(".")[::-1] + ["dnsbl.httpbl.org"]))
                if answer:
                    octets = [int(n) for n in answer[0].to_text().split(".")]
                    _type = octets[3]
                    info["ok"] = octets[0] == 127
                    info["found"] = True
                    info["last-seen-days"] = octets[1]
                    if _type != 0:
                        info["threat-score"] = octets[2]
                    else:
                        info["search-engine-id"] = octets[2]
                        info["type"]["search-engine"] = True
                        info["search-engine"] = self.search_engines[octets[2]]
                    for key, value in self.map.items():
                        if _type in value:
                            info["type"][key] = True
                return info
            except Exception as e:
                info["message"] = f"{e}"
        return info
