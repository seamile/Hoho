#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       alivepacket.py
#
# Copyright (c) 2009-2015 Seamile <lanhuermao@gmail.com>

from crypt import encrypt
from basicpacket import OutPacket

class AlivePacket(OutPacket):
    def __init__(self, qc, value):
        OutPacket.__init__(self)
        self.qc= qc

    def pack_0058(self):
        alv=self.qc.id+ self.qc.time
        self.body= encrypt(alv, self.qc.sessionkey)
