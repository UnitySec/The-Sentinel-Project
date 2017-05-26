# The Sentinel Project
## Notes: 
- You are going to need Python 3.6+ in order to run these scripts.
- All these scripts are made by me.

### Modules (./modules/):
 - haveibeenpwned.py: Single class module to interact with the [HaveIBeenPwned API](https://haveibeenpwned.com/API/).
 - heartbleed.py: Single class module to exploit the heartbleed bug on affected hosts ...
 - httpbl.py: Single class module to identify spammers and the spambots they use to scrape addresses from your website.
 - session.py: Single class module to simplify common HTTP(s) tasks (such as proxifying, getting and parsing responses, etc).
 - tor.py: Multi class module to interact with tor processes, hidden services, sockets, etc ...
 - utils.py: Basic terminal utils ...

### Scripts (./):
- apache-server-status.py: Retrieves and parses data from unprotected server-status pages on Apache web servers.
- crimeflare.py: [Uncovering bad guys hiding behind CloudFlare](http://crimeflare.com)!
- dnmap.py: DNS record Mapper.
- dns-zone-transfer.py: Requests a zone transfer (AXFR Query) from a DNS server.
- dnsbl.py: Identifies spammers and the spambots they use to scrape addresses from your website.
- eph-hs.py: Ephemeral hidden service (.onion) managing (create, list & close).
- fingerprintor.py: Retrieves descriptor (descriptive) information from hidden service addresses (.onion).
- heartbleed.py: Check and exploit the heartbleed bug ...
- pwn-test.py: [Check if you have an account that has been compromised in a data breach](https://haveibeenpwned.com/).
- tor-console.py: Interactive interpreter for interacting with Tor directly.
- tor.py: Tor process manager (start, list & kill) ...
- track.py: Basic host location tracker using the JSON API provided by [IP-API](http://ip-api.com).
- whois.py: Executes whois queries against whois servers (obviously).
