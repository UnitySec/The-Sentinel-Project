from modules import tor
from modules.utils import colored
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", action="store_true", help="List active hidden services.")
    parser.add_argument("-c", "--close", nargs="+", help="Discontinue the specified hidden service.")
    parser.add_argument("-p", "--ports", nargs="+", help="Hidden service port or map of hidden service port to their targets.")
    parser.add_argument("-d", "--discard-key", action="store_true", help="Avoid providing the key back in our response.")
    parser.add_argument("-k", "--private-key", type=argparse.FileType(), default=None, help="Key for the service to use.")
    args = parser.parse_args()
    
    try:
        if not tor.pids():
            print(colored("[i] Tor is actually not running, starting a new instance ...", "yellow"))
            Tor = tor.Tor()
            Tor.start(False, " -  ")
            print("")
        controller = tor.Controller()
        if args.list:
            ehs_list = sorted(controller.list_ephemeral_hidden_services([], detached=True))
            num = len(ehs_list)
            print(colored(f"[i] There {'is' if num == 1 else 'are'} {num or 'no'} ephemeral hidden service{'' if num == 1 else 's'} running at the momment."))
            for address in ehs_list:
                hs = tor.HiddenService(address, controller)
                print(colored(f" -  {hs.address} ({hs.descriptor_id})", dark=True))
        elif args.close:
            for address in sorted(set(args.close)):
                if address.endswith(".onion"):
                    address = address.split(".")[0]
                try:
                    hs = tor.HiddenService(address, controller)
                    discontinued = controller.remove_ephemeral_hidden_service(address)
                    print(colored(f"[+] {hs.address} ({hs.descriptor_id}): ") + (colored("Hidden Service not running in the first place ...", "yellow") if not discontinued else colored("Hidden Service successfully discontinued and closed.")))
                except Exception as e:
                    print(colored(f"[!] {address}.onion: {e}", "red"))
        elif args.ports:
            ports = {}
            for port in args.ports:
                if "=" in port:
                    number, target = port.split("=", 1)
                    ports[int(number)] = target
                else:
                    ports[int(port)] = int(port)
            print(colored("[i] Creating Hidden Service ..."))
            ehs = tor.EphemeralHiddenService(ports, args.discard_key, True, args.private_key, controller)
            print(colored(f"[i] Hidden Service running on {ehs.address}:"))
            print(colored(f" -  Publish Date & Time: {ehs.published}"))
            print(colored(f" -  Descriptor Identifier: {ehs.descriptor_id}"))
            print(colored(f" -  Descriptor Hash: {ehs.secret_id_part}"))
            print(colored(f" -  Descriptor Version: {ehs.version}"))
            print(colored(" -  Permanent Key: "))
            print(colored("    " + ehs.permanent_key.replace("\n", "\n    "), dark=True))
            print(colored(" -  Signature: "))
            print(colored("    " + ehs.signature.replace("\n", "\n    "), dark=True))
            print(colored(" -  Introduction Points:"))
            print(colored(f"      {' Identifier '.center(32, '-')}  {' Address '.center(21, '-')}", dark=True))
            for introduction_point in sorted(ehs.introduction_points(), key=lambda x: x.identifier):
                score = status = None
                print(colored(f"    - {introduction_point.identifier}: " + f"{introduction_point.address}:{introduction_point.port}", dark=True))
            print("")
            print(colored(" -  HS Port Map:"))
            for port, target in ports.items():
                print(colored(f"    - {port}: {target}", dark=True))
        else:
            parser.print_help()
    except Exception as e:
        print(colored(f"[!] {type(e).__name__}:", "red"))
        print(colored(f" -  {e}", "red", True))
    except KeyboardInterrupt:
        print(colored("[!] Keyboard Interrupted!", "red"))
