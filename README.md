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
- apache-server-status.py: Retrieves data from unprotected /server-status pages on Apache servers ...
- crimeflare.py: [Uncovering bad guys hiding behind CloudFlare](http://crimeflare.com)!
- dnsbl.py: HTTP:Bl based host checking script.
- dns-zone-transfer.py: Requests a zone transfer (AXFR Query) from a DNS server.
- fingerprintor.py: Retrieves (basic) descriptive information on Tor hidden services ...
- pwn-test.py: [Check if you have an account that has been compromised in a data breach](https://haveibeenpwned.com/).
- tor-console.py: [Stem](https://stem.torproject.org/) based console.
- track.py: Basic host location tracker using the JSON API provided by [IP-API](http://ip-api.com).
- whois.py: Executes whois queries against whois servers (obviously).
- heartbleed.py: Check/Exploit the heartbleed bug against HTTP, SMTP, IMAP, POP3, XMPP and FTP services running on a certain host or following a target list ...
