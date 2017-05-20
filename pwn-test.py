import argparse, time
from pprint import pprint
from modules.utils import *
from modules.haveibeenpwned import HIBP

def walk(resp):
    for result in resp:
        for key, value in result.items():
            if isinstance(value, str):
                print(colored(f" -  {key}: {value}", dark=True))
            elif isinstance(value, (tuple, list)):
                print(colored(f" -  {key}:", dark=True))
                print(colored("    - " + "\n    - ".join(value), dark=True))
            elif isinstance(value, dict):
                print(colored(f" -  {key}:", dark=True))
                print(colored("\n    - ".join(": ".join([k, v]) for k, v in value.items()), dark=True))
        print("")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--breach-search", metavar="account", type=str, help="Search the specified username or email address on public breaches ...")
    parser.add_argument("-p", "--paste-search", metavar="account", type=str, help="Search the specified username or email address on public pastes ...")
    parser.add_argument("-t", "--truncate-response", action="store_true", default=False, help="Truncate response to only the breach names instead of the entire breach object ...")
    parser.add_argument("-f", "--file", type=argparse.FileType(), help="Search the usernames/email addresses on the specified file (separated by newlines) for breached accounts ...")
    args = parser.parse_args()

    try:
        hibp = HIBP()
        if args.breach_search:
            resp = hibp.breach_search(args.breach_search, truncateResponse=args.truncate_response)
        elif args.paste_search:
            resp = hibp.paste_search(args.paste_search)
        elif args.file:
            for line in args.file:
                try:
                    line = line.strip()
                    if not line:
                        continue
                    resp = hibp.breach_search(line, truncateResponse=args.truncate_response)
                    #if resp.status_code != 404:
                    if resp.status_code == 200:
                        print(colored(f"[+] {line} - {', '.join([i['Name'] for i in resp.json()]) if resp.status_code == 200 else (hibp.codes[resp.status_code] if resp.status_code in hibp.codes else resp.reason)}"))
                    time.sleep(2)
                except Exception as e:
                    print(colored(f"[!] {type(e).__name__}:", "red"))
                    print(colored(f" -  {e}", "red", True))
                except KeyboardInterrupt:
                    print(colored("[!] Keyboard Interrupted!", "red"))
                    break
            exit()
        else:
            parser.print_help()
            exit()
        if resp.status_code != 200:
            if resp.status_code in hibp.codes:
                print(colored(f"[{resp.status_code}] {hibp.codes[resp.status_code]}", "red"))
        else:
            resp = resp.json()
            for i in range(len(resp)):
                if "Description" in resp[i]:
                    del resp[i]["Description"]
            print(colored(f"[i] Results ({len(resp)}):"))
            walk(resp)
    except Exception as e:
        print(colored(f"[!] {type(e).__name__}:", "red"))
        print(colored(f" -  {e}", "red", True))
    except KeyboardInterrupt:
        print(colored("[!] Keyboard Interrupted!", "red"))
