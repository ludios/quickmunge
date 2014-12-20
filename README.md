Some utilities for manipulating lines of text, numbers, JSON, bencode, and HTML fragments.  They're intended for use in shell pipes.

The black sheep are `munge-sets` and `munge-sets-interactively`, which load from files instead.

`decode-entities` requires BeautifulSoup 3.x.

`json-to-edn` requires https://github.com/swaroopch/edn_format

`linkify` requires https://github.com/jsocol/bleach

Everything else requires just Python 2.7.
