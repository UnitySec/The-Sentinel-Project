from modules.utils import *
import dns.query, dns.zone
import argparse, socket, os



class Script(object):
    def __init__(self, zone, where="", port=53, source=None, source_port=0, timeout=None, lifetime=None, use_udp=False,
                 rdtype="AXFR", rdclass="IN", af="AF_INET", serial=None, keyalgorithm=None, relativize=True, check_origin=True, save=False):
        self.name = zone
        self.save = save
        if not where:
            where = zone
        where = socket.gethostbyname(where)
        
        if rdtype not in [type for type in dir(dns.rdatatype) if type.isupper()]:
            raise ValueError(f"Unknown or invalid DNS Rdata Type \"{rdtype}\" ...")
        rdtype = getattr(dns.rdatatype, rdtype)
        
        if rdclass not in [type for type in dir(dns.rdataclass) if type.isupper()]:
            raise ValueError(f"Unknown or invalid DNS Rdata Class \"{rdclass}\" ...")
        rdclass = getattr(dns.rdataclass, rdclass)
        
        if af not in [i for i in dir(socket) if i.startswith("AF_")]:
            raise ValueError(f"Unknown or invalid Address Family \"{af}\" ...")
        address_family = int(getattr(socket, af))
        
        if keyalgorithm and keyalgorithm not in [alg for alg in dir(dns.tsig) if alg.startswith("HMAC_")]:
            raise ValueError(f"Unknown or invalid TSIG Algorithm \"{keyalgorithm}\" ...")
        keyalgorithm = dns.tsig.default_algorithm if not keyalgorithm else getattr(dns.tsig, keyalgorithm)
        
        
        self.config = {"query": {"zone": self.name, "where": where, "port": port, "source_port": source_port, "timeout": timeout, "lifetime": lifetime, "use_udp": use_udp},
                       "zone": {"check_origin": check_origin, "relativize": relativize}}
        self.config["query"].update({"rdtype": rdtype, "rdclass": rdclass, "af": address_family, "serial": serial, "keyalgorithm": keyalgorithm, "relativize": relativize})
        
        if source:
            self.config["query"]["source"] = source
    
    def run(self):
        zone = dns.zone.from_xfr(dns.query.xfr(**self.config["query"]), **self.config["zone"])
        if self.save:
            if not os.isdir("./dns-zones"):
                os.mkdir("./dns-zones/")
            zone.to_file(f"./dns-zones/{self.name}.txt", sorted=True)
        else:
            print(colored(zone.to_text().decode("ascii"), dark=True))



if __name__ == "__main__":
    parser = argparse.ArgumentParser("dns-zone-transfer", description="Requests a zone transfer (AXFR Query) from a DNS server.")
    parser.add_argument("zone", type=str, help="The name of the zone to transfer.")
    parser.add_argument("-w", "--where", type=str, default="", help="String containing an IPv4 or IPv6 address where to send the message.")
    parser.add_argument("-p", "--port", type=int, default=53, help="The port to which to send the message. The default is 53.")
    parser.add_argument("-s", "--source", type=str, default=None, help="Source address. The default is the wildcard address.")
    parser.add_argument("-sP", "--source-port", type=int, default=0, help="The port from which to send the message. The default is 0.")
    parser.add_argument("-t", "--timeout", type=int, default=None, help="The number of seconds to wait for each response message.")
    parser.add_argument("-l", "--lifetime", type=float, default=None, help="The total number of seconds to spend doing the transfer. If None, the default, then there is no limit on the time the transfer may take.")
    parser.add_argument("-u", "--use-udp", type=bool, default=False, help="Use UDP (only meaningful for IXFR).")
    
    parser.add_argument("--rdtype", type=str, default="AXFR", help="The type of zone transfer. The default is \"AXFR\".")
    parser.add_argument("--rdclass", type=str, default="IN", help="The class of the zone transfer. The default is \"IN\".")
    parser.add_argument("--af", "--address-family", type=str, default="AF_INET", help="the address family to use. The default is None, which causes the address family to use to be inferred from the form of where. If the inference attempt fails, AF_INET is used.")
    parser.add_argument("--serial", type=int, default=None, help="The SOA serial number to use as the base for an IXFR diff sequence (only meaningful if rdtype == \"IXFR\").")
    parser.add_argument("--keyalgorithm", type=str, default=None, help="The TSIG algorithm to use; defaults to \"{}\".".format(str(dns.tsig.default_algorithm)))
    parser.add_argument("--relativize", type=bool, default=True, help="If True, all names in the zone will be relativized to the zone origin.")
    parser.add_argument("--check-origin", type=bool, default=True, help="Should sanity checks of the origin node be done? The default is True.")
    parser.add_argument("--save", action="store_true", help="Save DNS Zone on ./dns-zones/{zone}.txt.")
    
    args = parser.parse_args()
    args = {arg: getattr(args, arg) for arg in dir(args) if arg[0] != "_"}
    
    try:
        script = Script(**args)
        script.run()
    except TypeError as e:
        if str(e) == "%u format: a number is required, not NoneType":
            print(colored("[!] Please specify a serial using --serial in order to complete the request ...", "red"))
    except Exception as e:
        print(colored(f"[!] Failed to retrieve the DNS Zone from \"{args['zone']}\":", "red"))
        print(colored("    " + str(e), "red", True))
