# The contents of this file are subject to the BitTorrent Open Source License
# Version 1.1 (the License).  You may not copy or use this file, in either
# source code or executable form, except in compliance with the License.  You
# may obtain a copy of the License at http://www.bittorrent.com/license/.
#
# Software distributed under the License is distributed on an AS IS basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.  See the License
# for the specific language governing rights and limitations under the
# License.

# Written by Petru Paler

# Modified for quickmunge by Ivan Kozik

from BTL import BTFailure

from collections import OrderedDict


def decode_int(x, f):
    f += 1
    newf = x.index(b"e", f)
    n = int(x[f:newf])
    if x[f] == 45: # "-"
        if x[f + 1] == 48: # "0"
            raise ValueError
    elif x[f] == 48 and newf != f + 1:
        raise ValueError
    return (n, newf + 1)

def decode_string(x, f):
    colon = x.index(b":", f)
    n = int(x[f:colon])
    if x[f] == 48 and colon != f + 1:
        raise ValueError
    colon += 1

    # Must use latin-1 to handle non-utf-8 bytestrings; Unicode codepoints
    # represent bytes.
    b = x[colon:colon + n]
    s = b.decode("latin-1")

    return (s, colon + n)

def decode_list(x, f):
    r, f = [], f + 1
    while x[f] != 101: # "e"
        v, f = decode_func[x[f]](x, f)
        r.append(v)
    return (r, f + 1)

def decode_dict(x, f):
    r = OrderedDict()
    f += 1
    while x[f] != 101: # "e"
        k, f = decode_string(x, f)
        r[k], f = decode_func[x[f]](x, f)
    return (r, f + 1)

decode_func = {}
decode_func[b"l"[0]] = decode_list
decode_func[b"d"[0]] = decode_dict
decode_func[b"i"[0]] = decode_int
decode_func[b"0"[0]] = decode_string
decode_func[b"1"[0]] = decode_string
decode_func[b"2"[0]] = decode_string
decode_func[b"3"[0]] = decode_string
decode_func[b"4"[0]] = decode_string
decode_func[b"5"[0]] = decode_string
decode_func[b"6"[0]] = decode_string
decode_func[b"7"[0]] = decode_string
decode_func[b"8"[0]] = decode_string
decode_func[b"9"[0]] = decode_string

def bdecode(x):
    try:
        r, l = decode_func[x[0]](x, 0)
    except (IndexError, KeyError, ValueError):
        raise BTFailure("not a valid bencoded string")
    if l != len(x):
        raise BTFailure("invalid bencoded value (data after valid prefix)")
    return r


class Bencached(object):

    __slots__ = ["bencoded"]

    def __init__(self, s):
        self.bencoded = s

def encode_bencached(x,r):
    r.append(x.bencoded)

def encode_int(x, r):
    r.extend((b"i", str(x).encode("latin-1"), b"e"))

def encode_bool(x, r):
    if x:
        encode_int(1, r)
    else:
        encode_int(0, r)
        
def encode_bytes(x, r):
    length_prefix = str(len(x)).encode("latin-1")
    r.extend((length_prefix, b":", x))

def encode_list(x, r):
    r.append(b"l")
    for i in x:
        encode_func[type(i)](i, r)
    r.append(b"e")

def encode_dict(x,r):
    r.append(b"d")
    for k, v in x.items():
        assert isinstance(k, str), k
        encode_func[type(k)](k, r)
        encode_func[type(v)](v, r)
    r.append(b"e")

encode_func = {}
encode_func[Bencached]   = encode_bencached
encode_func[int]         = encode_int
encode_func[bytes]       = encode_bytes
encode_func[list]        = encode_list
encode_func[tuple]       = encode_list
encode_func[dict]        = encode_dict
encode_func[OrderedDict] = encode_dict

try:
    encode_func[bool] = encode_bool
except ImportError:
    pass

def bencode(x):
    r = []
    encode_func[type(x)](x, r)
    return b"".join(r)
