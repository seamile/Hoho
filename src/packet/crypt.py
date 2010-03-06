#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       qqcrypt.py
"""
The MIT License

Copyright (c) 2005 hoxide

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

QQ Crypt module.

"""
from struct import pack as _pack
from struct import unpack as _unpack
from binascii import b2a_hex, a2b_hex

from random import seed
from random import randint as _randint

__all__ = ['encrypt', 'decrypt' ,'randkey']

seed()

op = 0xffffffffL

def xor(a, b):
    a1,a2 = _unpack('>LL', a[0:8])
    b1,b2 = _unpack('>LL', b[0:8])
    r = _pack('>LL', ( a1 ^ b1) & op, ( a2 ^ b2) & op)
    return r

def code(v, k):
    """TEA 加密
    64比特明码, 128比特密钥, qq的TEA算法使用16轮迭代
    """
    n=16  #qq use 16
    delta = 0x9e3779b9L
    k = _unpack('>LLLL', k[0:16])
    y, z = _unpack('>LL', v[0:8])
    s = 0
    for i in xrange(n):
        s += delta
        y += (op &(z<<4))+ k[0] ^ z+ s ^ (op&(z>>5)) + k[1] ;
        y &= op
        z += (op &(y<<4))+ k[2] ^ y+ s ^ (op&(y>>5)) + k[3] ;
        z &= op
    r = _pack('>LL',y,z)
    return r

def decipher(v, k):
    """TEA 解密程序
    用128比特密钥, 解密64比特值
    """
    n = 16
    y, z = _unpack('>LL', v[0:8])
    a, b, c, d = _unpack('>LLLL', k[0:16])
    delta = 0x9E3779B9L;
    s = (delta << 4)&op
    for i in xrange(n):
        z -= ((y<<4)+c) ^ (y+s) ^ ((y>>5) + d)
        z &= op
        y -= ((z<<4)+a) ^ (z+s) ^ ((z>>5) + b)
        y &= op
        s -= delta
        s &= op
    return _pack('>LL', y, z)

def encrypt(v, k):
    """QQ消息加密"""
    ##FILL_CHAR = chr(0xAD)
    k=a2b_hex(k)
    v=a2b_hex(v)
    END_CHAR = '\0'
    FILL_N_OR = 0xF8
    vl = len(v)
    filln = (8-(vl+2))%8 + 2;
    fills = ''
    for i in xrange(filln):
        fills = fills + chr(_randint(0, 0xff))
    v = ( chr((filln -2)|FILL_N_OR)
          + fills
          + v
          + END_CHAR * 7)
    tr = '\0'*8
    to = '\0'*8
    r = ''
    o = '\0' * 8
    #print 'len(v)=', len(v)
    for i in xrange(0, len(v), 8):
        o = xor(v[i:i+8], tr)
        tr = xor( code(o, k), to)
        to = o
        r += tr
    return b2a_hex(r)

def decrypt(v, k):
    """QQ消息解密"""
    k=a2b_hex(k)
    v=a2b_hex(v)
    l = len(v)
    #if l%8 !=0 or l<16:
    #    return ''
    prePlain = decipher(v, k)
    pos = (ord(prePlain[0]) & 0x07L) +2
    r = prePlain
    preCrypt = v[0:8]
    for i in xrange(8, l, 8):
        x = xor(decipher(xor(v[i:i+8], prePlain),k ), preCrypt)
        prePlain = xor(x, preCrypt)
        preCrypt = v[i:i+8]
        r += x
    if r[-7:] != '\0'*7: return None

    return b2a_hex(r[pos+1:-7])

def randkey(n):
    """生成n位十六进制的随机值"""
    key=''
    for i in xrange(n):
        key+='%02x'%_randint(0,255)
    return key

def _test():
    import doctest, crypt
    return doctest.testmod(crypt)
if __name__ == "__main__":_test()
