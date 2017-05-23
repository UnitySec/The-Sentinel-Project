from modules.heartbleed import Heartbleed
from modules.utils import colored
import argparse, os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str, help="Target URL: (e.g: 'http://hostname.ext:4433/', 'smtp://hostname.ext/')")
    parser.add_argument("-t", "--timeout", type=float, default=8, help="Timeout on socket operations (in seconds).")
    parser.add_argument("-d", "--dump-dir", type=str, default="", help="Directory to save dumped data on (Does not saves dump data if this have not been specified).")
    parser.add_argument("-f", "--file", type=argparse.FileType(), help="Target list (Sep. by newlines).")
    args = parser.parse_args()
    
    if args.url:
        try:
            h = Heartbleed(args.url, args.timeout, args.dump_dir, quiet=False)
            h.check()
        except Exception as e:
            print(colored(f"[!] {type(e).__name__}:", "red"))
            print(colored(f" -  {e}", "red", True))
        except KeyboardInterrupt:
            print(colored("[!] Keyboard Interrupted! (Ctrl+C Pressed)", "red"))
    elif args.file:
        lines = [line.strip() for line in args.file.readlines() if line.strip()]
        targets = sorted(set(lines))
        max_len = max([len(target) for target in targets])
        print(colored(f"[i] A total of {len(targets)} unique targets are going to checked ..."))
        for target in targets:
            try:
                h = Heartbleed(target, args.timeout, args.dump_dir)
                vuln = h.check()
                print(colored(f"[{'+' if vuln else '-'}] {target.ljust(max_len + 3)}{'V' if vuln else 'Not v'}ulnerable to Heartbleed!", "green" if vuln else "yellow"))
            except Exception as e:
                print(colored(f"[!] {target.ljust(max_len + 3)}{type(e).__name__.replace('_', ' ').title()}: {e if len(str(e)) < 45 else str(e)[:45] + '[...]'}", "red"))
            except KeyboardInterrupt:
                print(colored("[!] Keyboard Interrupted!", "red"))
                break
    else:
        parser.print_help()
