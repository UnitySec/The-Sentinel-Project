from argparse import ArgumentParser
from modules.utils import *
import requests, socket



def track(host):
    globe = ["            ,,,,,,            ",
             "        o#'9MMHb':'-,o,       ",
             "     .oH\":HH$' \"' ' -*R&o,    ",
             "    dMMM*\"\"'`'      .oM\"HM?.  ",
             "  ,MMM'          \"HLbd< ?&H\  ",
             " .:MH .\"\          ` MM  MM&b ",
             ". \"*H    -        &MMMMMMMMMH:",
             ".    dboo        MMMMMMMMMMMM.",
             ".   dMMMMMMb      *MMMMMMMMMP.",
             ".    MMMMMMMP        *MMMMMP .",
             "     `#MMMMM           MM6P , ",
             " '    `MMMP\"           HM*`,  ",
             "  '    :MM             .- ,   ",
             "   '.   `#?..  .       ..'    ",
             "      -.   .         .-       ",
             "        ''-.oo,oo.-''         "]
    try:
        resp = requests.get(f"http://ip-api.com/json/{host}?fields=258047").json()
        if resp["status"] == "fail":
            raise Exception(f"{' - '.join(f'{key.title()}: {value}' for key, value in resp.items())}")
        else:
            info = [" Tracking Results ".center(35, "-"),
                    f'        IP Address {resp["query"]}',
                    f'           Country {resp["country"]}/{resp["countryCode"]}',
                    f'            Region {resp["regionName"]}/{resp["region"]}',
                    f'              City {resp["city"]}',
                    f'          Zip Code {resp["zip"]}',
                    f'         Time Zone {resp["timezone"]}',
                    f'      Organization {resp["org"]}',
                    f'               ISP {resp["isp"]}',
                    f'          Latitude {resp["lat"]}',
                    f'         Longitude {resp["lon"]}',
                    f'          Is Proxy {resp["proxy"]}',
                    f'         Is Mobile {resp["mobile"]}',
                    f'         {resp["as"]}']
            
            for line in globe:
                index = globe.index(line)
                
                try:
                    if index in [1, 14]:
                        print(colored(f"     {line}  {info[index-1]}"))
                    elif index > 1 and index < 14:
                        print(f"     {colored(line)}  {colored(info[index-1], dark=True)}")
                    else:
                        print(colored(" " * 5 + line))
                except Exception as e:
                    print(colored(" " * 5 + line))
    except Exception as e:
        print(colored(f"[!] Failed to track {repr(host)}:", "red"))
        print(colored(" -  " + str(e), "red", True))



if __name__ == "__main__":
    parser = ArgumentParser(description="This is a basic host location tracker using the JSON API provided by ip-api.com.")
    parser.add_argument("host", type=str, help="Target hostname or IP Address ...")
    
    args = parser.parse_args()
    track(args.host)
