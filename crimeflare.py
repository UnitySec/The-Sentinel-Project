from dns.resolver import Resolver
from modules.utils import *
from modules.session import Session
import re



class CrimeFlare(Session):
    def __init__(self, *args, **kwargs):
        super(CrimeFlare, self).__init__("http://www.crimeflare.com/")
        self.resolver = Resolver()
    
    def cfsearch(self, domain: str):
        try:
            nameservers = [ns.to_text() for ns in self.resolver.query(domain, "NS")]
            
            resp = self.request("POST", "/cgi-bin/cfsearch.cgi", data={"cfS": domain})
            page = self.parse_html(resp.text)
            cfl_ids = [a.get("href") for a in page.findAll("a", attrs={"href": re.compile(r"^http://www.crimeflare.com/cgi-bin/cflist/.*$")})]
            
            print(colored("[i] CloudFlare Search Results:"))
            print(colored(" -  Name Servers:"))
            for ns in nameservers:
                print(colored("    - {} [{}]".format(ns, ", ".join(ip.to_text() for ip in self.resolver.query(ns, "A"))), dark=True))
            print("")
            if cfl_ids:
                print(colored(" -  CFList (CFL) IDs: (One use only)"))
                for id in cfl_ids:
                    print(colored("    - " + id.split("/")[-1], dark=True))
                print("")
            if page.ul:
                print(colored(" -  " + "\n -  ".join(page.ul.stripped_strings), dark=True))
            else:
                print(colored(" -  No direct-connect IP addresses have been found for this domain ...", "red", True))
        except KeyboardInterrupt:
            print(colored("[!] Keyboard Interrupted (Ctrl+C [KeyboardInterrupt])", "red"))
        except Exception as e:
            err_name = type(e).__name__
            print(colored(f"[!] {err_name}:", "red"))
            print(colored(f" -  {e}", "red", True))
    
    def cflist(self, cfl_id: str):
        try:
            resp = self.request("GET", "/cgi-bin/cflist/" + cfl_id, headers={"Referer": "http://www.crimeflare.com/cgi-bin/cfsearch.cgi"})
            page = BeautifulSoup(resp.text, "html.parser")
            if page.title.text.lower() == "cloudflare search results":
                domains = list(page.stripped_strings)[3:-4]
                print(colored("[i] Some CloudFlare-User domains with a direct-connect IP address of {}:".format(cfl_id.split("-")[1])))
                for i in range(0, len(domains), 2):
                    print(colored(" -  {:32}{:32}".format(*domains[i:i+2], ""), dark=True))
            else:
                raise Exception("Failed to list cloudflare-user domains with this CFL id ...")
        except KeyboardInterrupt:
            print(colored("[!] Keyboard Interrupted (Ctrl+C [KeyboardInterrupt])", "red"))
        except Exception as e:
            err_name = type(e).__name__
            print(colored(f"[!] {err_name}:", "red"))
            print(colored(f" -  {e}", "red", True))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="crimeflare.com - Uncovering bad guys hiding behind CloudFlare ...")
    parser.add_argument("-s", "-cfs", "--search", type=str, help="CloudFlare \"Protected\" Domain Search ...")
    parser.add_argument("-l", "-cfl", "--list", type=str, help="List CloudFlare domains using the specified Direct-Connect IP Address ...")
    parser.add_argument("-x", "--proxy", default="", type=str, help="Proxify session through this proxy ('proto://ip.add.re.ss:port/') ...")
    args = parser.parse_args()
    
    cf = CrimeFlare()
    if args.proxy:
        cf.proxies.update({"http": args.proxy, "https": args.proxy})
    
    if args.search:
        cf.cfsearch(args.search)
    elif args.list:
        cf.cflist(args.list)
    else:
        parser.print_help()
