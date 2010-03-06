#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       MsgPacket.py
#
# Copyright (c) 2009-2015 Seamile <lanhuermao@gmail.com>

from binascii import a2b_hex,b2a_hex
from crypt import encrypt
from basicpacket import OutPacket

class MsgPacket(OutPacket):
    def __init__(self, qc, value):
        '''字体，大小，粗细，斜体，下划线，颜色
           font=[type,size,bold,italic,underline,color]'''
        OutPacket.__init__(self)
        self.qc= qc
        self.value=value
        self.font= 'SUN'
        self.size= 10
        self.bold= 0
        self.italic= 0
        self.underline= 0
        self.color= 'BLACK'

    def pack_00cd(self):
        msg=raw_input('输入消息 >').decode('gbk').encode('utf8')
        length_1='%04x'%len(msg)
        length_2='%04x'%(len(msg)+3)
        msg=length_2+'01'+length_1+b2a_hex(msg)
        verify= self.qc.md5(a2b_hex(self.value+self.qc.sessionkey))
        timeNow= self.qc.localTime()

        body=self.qc.id+ self.value+\
             '000000080001000400000000190F'+\
             self.qc.id+ self.value+\
             verify+\
             '000b4033'+\
             timeNow+\
             '007E000000010100000001'+\
             '4D53470000000000'+\
             timeNow+\
             '3C51BE0B00000000090086000006E5AE8BE4BD93000001'+\
             msg
        self.body= encrypt(body, self.qc.sessionkey)

    def pack_0017(self):
        self.body= encrypt(self.value, self.qc.sessionkey)
