from argparse import ArgumentParser
from html2text import html2text
from modules.utils import *
from modules.session import Session
import os


__doc__ = "Retrieves and parses data from unprotected server-status pages on Apache web servers."

class Script(Session):
    def __init__(self, url):
        if "://" not in url:
            url = f"http://{url}/"
        super(Script, self).__init__(url)
    
    def run(self):
        response = self.request("GET", f"/server-status")
        
        soup = self.parse_html(response.text)
        if soup.title.text.lower() != "apache status" or response.status_code != 200:
            raise Exception("Failed to retrieve any data from the '/server-status' page ...")
        
        print(colored(f"[i] {soup.h1.text}"))
        if soup.address:
            print(colored(f" -  {soup.address.text}"))
        info = [i.text.encode("ascii", errors="replace").decode("ascii") for i in soup.findAll("dl")]
        for i in info:
            for i in i.split("\n"):
                k, *v = i.split(":")
                if v:
                    print(colored(" {}  {}:{}".format("-" if k or v else "", colored(k), colored(":".join(v), dark=True))))
                else:
                    print(colored(" {}  {}".format("-" if k or v else "", k)))
        print(colored("    " + soup.pre.text.replace("\n", "\n    "), dark=True))
        print("")
        print(colored(" -  {}\n".format(self.parse_html(str(soup).split("<p>")[1].split("<p />")[0]).text.replace("\n", "\n    ")), dark=True))
        print("\n")
        
        logs, logs_help, *other = soup.findAll("table")
        filename = f"./logs/{self.base_url.netloc.replace(':', '-')}-logs.csv"
        if not os.path.isdir("./logs/"):
            os.mkdir("./logs/")
        open(filename, "w").write("\n".join(", ".join(log.stripped_strings) for log in logs.findAll("tr")))
        print(colored(f" -  Server logs have been saved as CSV on \"{filename}\"."))
        print(colored(" -  Log keys description:"))
        print(colored("    {}".format("\n    ".join(["{}: {}".format(*i.stripped_strings) for i in logs_help.findAll("tr")])), dark=True))
        print("")

        for table in other:
            rows = table.findAll("tr")
            print(colored(f" -  {rows[0].font.text}"))
            print(colored("    - " + "\n    - ".join([row for row in html2text(str(rows[1])).replace("**", "").split("\n") if row]), dark=True))



if __name__ == "__main__":
    parser = ArgumentParser(__doc__)
    parser.add_argument("target", type=str, help="Target webserver address or url")
    args = parser.parse_args()
    try:
        script = Script(args.target)
        script.run()
    except Exception as e:
        print(colored(f"[!] Failed to retrieve server-status page info from \"{args.target}\":", "red"))
        print(colored(" -  " + str(e), "red", True))
