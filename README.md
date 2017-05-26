# The Sentinel Project
## Notes: 
- You are going to need Python 3.6+ in order to run these scripts.
- All these scripts are made by me.

### Modules (./modules/):
- utils.py: Simple (small and almost useless) utils to be used on scripts ...
- tor.py: Multi Class Module to interact with tor processes, hidden services and sockets ...
- session.py: Module (Single Class) to simplify the work with HTTP(S) sessions ...
- httpbl.py: Module (Single Class) to interact with the HTTP:Bl API from the [Project Honey Pot](projecthoneypot.org) ...
- haveibeenpwned.py: Module (Single Class) to interact with the [HaveIBeenPwned](https://haveibeenpwned.com/) API ...
- heartbleed.py: Module to exploit the heartbleed bug on affected hosts ...

### Scripts (./):
- apache-server-status.py: Retrieves and parses data from unprotected server-status pages on Apache web servers.
- crimeflare.py: [Uncovering bad guys hiding behind CloudFlare](http://crimeflare.com)!
- dnmap.py: DNS record Mapper.
- dns-zone-transfer.py: Requests a zone transfer (AXFR Query) from a DNS server.
- dnsbl.py: Identifies spammers and the spambots they use to scrape addresses from your website.
- eph-hs.py: Ephemeral hidden service (.onion) managing (create, list & close).
- fingerprintor.py: Retrieves descriptor (descriptive) information from hidden service addresses (.onion).
- heartbleed.py: Check and exploit the heartbleed bug ...
- help.py: None
- pwn-test.py: [Check if you have an account that has been compromised in a data breach](https://haveibeenpwned.com/).
- tor-console.py: Interactive interpreter for interacting with Tor directly.
- tor.py: Tor process manager (start, list & kill) ...
- track.py: Basic host location tracker using the JSON API provided by [IP-API](http://ip-api.com).
- whois.py: Executes whois queries against whois servers (obviously).
