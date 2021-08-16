from modules import tor
from modules.utils import colored
import argparse, signal, json, os


__doc__ = "Tor process manager (start, list & kill) ..."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("-c", "--config", type=argparse.FileType(), metavar="File", help="Config file (.json).")
    parser.add_argument("-k", "--kill", type=int, metavar="PID", nargs="+", help="Kill/Close tor processes (from pids).")
    parser.add_argument("-l", "--list", action="store_true", help="List active tor processes.")
    args = parser.parse_args()
    
    try:
        pids = tor.pids()
        num = len(pids)
        if args.list:
            print(colored(f"[i] There {'is' if num == 1 else 'are'} {num or 'no'} Tor process{'' if num == 1 else 'es'} running at the momment."))
            for pid in pids:
                print(colored(f" -  PID: {pid} ({hex(pid)})", dark=True))
        elif args.kill:
            for pid in sorted(set(args.kill)):
                try:
                    os.kill(pid, signal.SIGTERM)
                    print(colored(f"[+] Tor process with pid {pid} successfully killed."))
                except Exception as e:
                    print(colored(f"[!] Failed to close Tor process with pid {pid}: {e}", "red"))
        else:
            config = json.load(args.config) if args.config else {}
            print(colored("[i] Starting Tor process ...", "yellow"))
            Tor = tor.Tor()
            Tor.start(False, " -  ")
            print(colored(f"[i] Process running with PID: {Tor.process.pid}"))
    except Exception as e:
        print(colored(f"[!] {type(e).__name__}:", "red"))
        print(colored(f" -  {e}", "red", True))
    except KeyboardInterrupt:
        print(colored("[!] Keyboard Interrupted!", "red"))
