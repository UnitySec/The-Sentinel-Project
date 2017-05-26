from modules import session
import time, argparse


__doc__ = "Single class module to interact with the HaveIBeenPwned (haveibeenpwned.com) API."

class HIBP(session.Session):
    def __init__(self, version=2):
        super(HIBP, self).__init__(f"https://haveibeenpwned.com/api/v{version}/")
        self.codes = {200: "Ok — Everything worked and there's a string array of pwned sites for the account.",
                      400: "Bad request — The account does not comply with an acceptable format. (i.e. it's an empty string)",
                      403: "Forbidden — No user agent has been specified in the request.",
                      404: "Not found — The account could not be found and has therefore not been pwned.",
                      429: "Too many requests — The rate limit has been exceeded."}
        self.paste_search = lambda account: self.request("GET", f"pasteaccount/{account}")
        self.breach_search = lambda account, domain="", truncateResponse=False: self.request("GET", f"breachedaccount/{account}?{f'domain={domain}&' if domain else ''}truncateResponse={truncateResponse}")
        self.breaches = lambda domain="": self.request("GET", f"breaches?{f'domain={domain}&' if domain else ''}")
        self.breach = lambda name: self.request("GET", f"breach/{name}")
        self.dataclasses = lambda: self.request("GET", "dataclasses")
