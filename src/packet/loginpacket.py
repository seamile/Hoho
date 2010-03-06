#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       LoginPacket.py
#
# Copyright (c) 2009-2015 Seamile <lanhuermao@gmail.com>

import data
from crypt import encrypt,randkey
from basicpacket import OutPacket

class LoginPacket(OutPacket):
    """Login Packets"""
    verify_PNG=''
    def __init__(self,qc,value):
        OutPacket.__init__(self)
        self.qc= qc
        self.value=value
        data.loginData['krand']= randkey(16) #初始化随机密钥

    def pack_0091(self):
        code= '0001'+ data.str1+ data.str2+ '00'*15
        code= encrypt(code, data.loginData['krand'])
        self.body= data.loginData['krand']+ code

    def pack_00ba(self):
        if not self.value:
            code= '0001'+ data.str1+ data.str2+ data.loginData['tk91']+ '03000500000000000000'
            code=encrypt(code, data.loginData['krand'])
            self.body= data.loginData['krand']+ code
        else:
            verify=raw_input('请输入验证码：')

    def pack_00dd(self):
        '''0xdd的发送包还不完美，有待进一步分析'''
        #inf为120字节的验证信息
        inf1= 'b37985fa'# 随机？
        inf2= '0001'
        inf3= self.qc.id
        inf5= '000001'
        inf6= self.qc.md5ps1
        inf7= self.qc.time
        inf8= '00'*13
        inf9= self.qc.myip
        inf10= '00'*9+'10'#结尾的10可能是长度
        # 这里应该是一个 random
        inf11= self.qc.md5ps1
        # 解0xdd返回包的Key，这里固定为md5ps1， 应该也是一个Randkey
        inf12= self.qc.md5ps1
        inf=inf1+ inf2+ inf3+ data.str2+ inf5+ inf6+ inf7+ inf8+ inf9+ inf10+ inf11+ inf12
        inf=encrypt(inf, self.qc.md5ps2)#这段验证信息，用md5ps2加密

        code1= '00ca0001' +data.str1 +data.str2
        code2= '0078'
        code3= '0000018B2E0100004823001'+'00'*17+'2000018BE0010'
        fill= '00'*364

        code= code1+ data.loginData['tkba']+ code2+ inf+ code3+ fill

        code=encrypt(code, data.loginData['krand'])
        self.body= data.loginData['krand']+ code

    def pack_00e5(self):
        code1= '010D000101'+ data.str1 +data.str2
        code2= data.loginData['tkba']
        code3= '0020'
        code4= data.loginData['tkdd'][0]
        code5= '00'*6
        code= code1+ code2+ code3+ code4+ code5
        code= encrypt(code, data.loginData['kdd'][0])
        self.body= data.loginData['tkdd'][1]+ code

    def pack_0030(self):
        code='0001'+ data.str2+ '00c80002'+ \
             self.qc.time+ \
             self.qc.myip+ '00000000'+ data.loginData['tke5']+ '00'*35+ data.sp4md5+\
             '84'+\
             '0a'+\
             '00'*10+\
             '01000106'+\
             '00'*11+\
             data.str1+ '00'*16+ data.loginData['tkba']+ '0000000700000000080410014001'+\
             '00004AE10010'+'00'*26+\
             '01000106'+'00'*11+'0200003D6C0010'+'00'*16+\
             '00'*249
        self.body= data.loginData['tkdd'][1]+ encrypt(code, data.loginData['kdd'][0])
