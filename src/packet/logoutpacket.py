#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       LogOutPacket.py
#
# Copyright (c) 2009-2015 Seamile <lanhuermao@gmail.com>

from crypt import encrypt
from basicpacket import OutPacket

class LogOutPacket(OutPacket):
    """登出包"""
    def __init__(self,client,value):
        OutPacket.__init__(self)
        self.qc= client

    def pack_0062(self):
        outkey='00'*16
        self.body= encrypt(outkey, self.qc.sessionkey)
