domainmagic
===========

domainmagic is a library which combines a bunch of domain/dns lookup tools and stuff often used in related applications

Overview
________

Generic features
________________

- parallel processing (threadpool, parallel dns lookups, ...)
- automatic file updates (geoip database, iana tld list, ...)


Domain/DNS/...
______________

- validator functions (ip adresses, hostnames, email addresses)
- uri and email address extraction
- tld/2tld/3tld handling
- rbl lookups
- geoIP 


Installation
____________

Supported version of Python:
- python 3.6
- python 3.7
- python 3.8

Depencendies:
- geoip2
- dnspython

```
python setup.py install
```


