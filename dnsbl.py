from modules import httpbl
from modules.utils import pprint, colored
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str, help="Target hostname or ip address.")
    parser.add_argument("-k", "--api-key", type=str, default="vztjisbgwwij", help="Your HTTP:Bl Access Key.")
    args = parser.parse_args()

    try:
        dnsbl = httpbl.DNSbl(args.api_key)
        info = dnsbl.query(args.host)
        if info["message"]:
            raise Exception(info["message"])
        print(colored("[i] DNSbl query results:"))
        pprint(info, 1, lambda x: x, "green", True)
    except Exception as e:
        print(colored(f"[!] {type(e).__name__}:", "red"))
        print(colored(f" -  {e}", "red", True))
    except KeyboardInterrupt:
        print(colored(f"[!] Keyboard Interrupted!", "red"))
