import dns.resolver, dns.message, argparse
from modules.utils import *


__doc__ = "DNS record Mapper."

class DNMap(dns.resolver.Resolver):
    def __init__(self):
        super(DNMap, self).__init__()
        self._nameservers = self.nameservers
        self.rdclasses = dict(sorted([(k, v) for k, v in dns.rdataclass.__dict__.items() if k.isupper()], key=lambda x: x[0]))
        self.rdtypes = dict(sorted([(k, v) for k, v in dns.rdatatype.__dict__.items() if k.isupper()], key=lambda x: x[0]))
        self._max_rdclass_length = max([len(rdclass) for rdclass in self.rdclasses])
        self._max_rdtype_length = max([len(rdtype) for rdtype in self.rdtypes])

    def _iter(self, answer):
        for record in sorted(answer, key=lambda x: dns.rdatatype.to_text(x.rdtype)):
            string = f" -  {dns.rdatatype.to_text(record.rdtype).ljust(self._max_rdtype_length)}"#f" -  {answer.canonical_name.to_text()}  {self.rdataclasses[record.rdclass].ljust(self._max_rdataclass_length)}  {self.rdatatypes[record.rdtype].ljust(self._max_rdatatype_length)}"
            print(colored(string), end="")
            extra = False
            for name in dir(record):
                value = getattr(record, name)
                if not name.startswith("_") and name not in ["rdtype", "rdclass"] and not callable(value):
                    s = f"{(' ' * len(string)) if extra else ''}{name}: "
                    if isinstance(value, bytes):
                        value = value.decode("ascii", errors="replace")
                    elif isinstance(value, (list, tuple)):
                        value = ("\n" + (" " * len(s))).join(sorted([i.decode("ascii", errors="replace") if isinstance(i, bytes) else str(i) for i in value]))
                    print(colored(s + f"{value}", dark=True))
                    extra = True
    
    def metaquery(self, qname, rdtype, rdclass=1, use_edns=None, want_dnssec=False, ednsflags=None, payload=None, request_payload=None, options=None,
                  timeout=8, port=53, af=None, source=None, source_port=0, ignore_unexpected=False, one_rr_per_rrset=False, tcp=False):
        try:
            ns = self.query(self.query(qname, "NS")[0].to_text()[:-1])[0].to_text()
        except:
            if self.nameservers:
                ns = self.nameservers[0]
            else:
                ns = "8.8.8.8"
        message = dns.message.make_query(qname, rdtype, rdclass, use_edns, want_dnssec, ednsflags, payload, request_payload, options)
        if tcp:
            resp = dns.query.tcp(message, ns, timeout=timeout, port=port, af=af, source=source, source_port=source_port, one_rr_per_rrset=one_rr_per_rrset)
        else:
            resp = dns.query.udp(message, ns, timeout=timeout, port=port, af=af, source=source, source_port=source_port, ignore_unexpected=ignore_unexpected, one_rr_per_rrset=one_rr_per_rrset)
        return resp
    
    def scan(self, host, **kwargs):
        print(colored(f"[i] Executing DNMap against {repr(host)} ..."))
        answer = self.metaquery(host, "ANY", **kwargs).answer
        if answer:
            self._iter(answer)
        else:
            for name, rdtype in self.rdtypes.items():
                if not dns.rdatatype.is_metatype(rdtype):
                    try:
                        answer = self.metaquery(host, rdtype, **kwargs).answer
                        if answer:
                            self._iter(answer)
                    except Exception as e:
                        print(colored(f" -  {name.ljust(self._max_rdtype_length)}") + colored(f"{e}", "red", dark=True))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("query", type=str, help="The query.")
    parser.add_argument("-t", "--timeout", type=int, default=8, help="The number of seconds to wait before the query times out.")
    parser.add_argument("-p", "--port", type=int, default=53, help="The port to which to send the message. The default is 53.")
    parser.add_argument("-i", "--ignore-unexpected", action="store_true", default=None, help="If True, ignore responses from unexpected.")
    parser.add_argument("-o", "--one-rr-per-rrset", action="store_true", default=None, help="Put each RR into its own RRset.")
    parser.add_argument("-e", "--use-edns", type=int, default=-1, help="The EDNS level to use. The default is -1 (no EDNS).")
    parser.add_argument("-s", "--want-dnssec", action="store_true", default=None, help="Should the query indicate that DNSSEC is desired?")
    args = parser.parse_args().__dict__
    
    dnmap = DNMap()
    try:
        dnmap.scan(args.pop("query"), **args)
    except Exception as e:
        print(colored(f" -  {e}", "red", True))
    except KeyboardInterrupt:
        print(colored("\n[!] Keyboard Interrupted!", "red"))
