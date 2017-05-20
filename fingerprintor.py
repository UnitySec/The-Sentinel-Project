from modules import tor
from stem.util import term
import argparse, socket, time


if __name__ == "__main__":
    Tor = None
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=str, help="Target hidden service address.")
    args = parser.parse_args()
    target = args.target
    
    try:
        if not tor.pids():
            print(term.format("[i] Tor is actually not running, starting a new temporary instance ...", "yellow"))
            Tor = tor.Tor()
            Tor.start(False, " -  ")
            print("")
        hs = tor.HiddenService(target)
        print(term.format("[i] Hidden Service Descriptive Info.:", "green"))
        print(term.format(f" -  Publish Date & Time: {hs.published}", "green"))
        print(term.format(f" -  Descriptor Identifier: {hs.descriptor_id}", "green"))
        print(term.format(f" -  Descriptor Hash: {hs.secret_id_part}", "green"))
        print(term.format(f" -  Descriptor Version: {hs.version}", "green"))
        print(term.format(f" -  Supported Versions: {', '.join(str(v) for v in hs.protocol_versions)}", "green"))
        print(term.format(" -  Permanent Key: ", "green"))
        print(term.format("    " + hs.permanent_key.replace("\n", "\n    "), "green"))
        print(term.format(" -  Signature: ", "green"))
        print(term.format("    " + hs.signature.replace("\n", "\n    "), "green"))
        print(term.format(" -  Introduction Points:", "green"))
        print(term.format(f"      {' Identifier '.center(32, '-')}  {' Address '.center(21, '-')}", "green"))
        for introduction_point in sorted(hs.introduction_points(), key=lambda x: x.identifier):
            score = status = None
            print(term.format(f"    - {introduction_point.identifier}: " + f"{introduction_point.address}:{introduction_point.port}", "green"))
    except Exception as e:
        print(term.format(f"[!] {type(e).__name__}:", "red"))
        print(term.format(f" -  {e}", "red"))
    except KeyboardInterrupt:
        print(term.format("[!] Keyboard Interrupted!", "red"))
    if Tor:
        Tor.exit()
