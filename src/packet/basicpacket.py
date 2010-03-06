#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       basicpacket.py
#
# Copyright (c) 2009-2015 Seamile <lanhuermao@gmail.com>

from random import randint
from binascii import a2b_hex

class Packet:
    sequences= []
    def __init__(self):
        self.head= ''
        self.body= ''
        self.tail= '03'

class OutPacket(Packet):
    """发送包基类"""
    def __init__(self):
        Packet.__init__(self)

    def newSequence(self,seq):
        if not seq:
            seq= '%04x'%randint(1,65534)
            if seq in Packet.sequences:
                return self.newSequence(None)
            else:
                Packet.sequences.append(seq)
                return seq
        else:
            return seq

    def newHead(self, cmd, seq):
        return '02190f'+ cmd+ self.newSequence(seq) + self.qc.id

    def newBody(self, cmd):
        try:
            getattr(self,'pack_%s'%cmd)()
            return self.body
        except:
            print '\n生成%s包失败。'%cmd

    def newPacket(self, cmd, seq):
        return a2b_hex( self.newHead(cmd,seq)+ self.newBody(cmd)+ self.tail )
