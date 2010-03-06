#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       client.py
#
# Copyright (c) 2009-2015 Seamile <lanhuermao@gmail.com>

import time
from hashlib import new
from binascii import a2b_hex

class Client:
    """ Client类 """
    def __init__(self):
        self.id= '%08x'%int(raw_input("输入QQ号：") )
        self.psw= raw_input('输入密码：')
        self.md5ps1= self.md5(self.psw)
        self.md5ps2= self.md5(a2b_hex(self.md5ps1))
        self.time= self.localTime()
        self.sessionkey='00'*16

    def localTime(self):
        return '%8x'%time.time()

    def md5(self,value):
        return new("md5",value).hexdigest()
