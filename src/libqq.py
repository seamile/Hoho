#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       libqq.py
#
# Copyright (c) 2009-2015 Seamile <lanhuermao@gmail.com>

from packet.loginpacket import LoginPacket
from packet.alivepacket import AlivePacket
from packet.msgpacket import MsgPacket
from packet.logoutpacket import LogOutPacket
from network import *

class Protocol:
    """QQ协议"""
    def __init__(self, qqclient, connect):
        self.qc= qqclient
        self.conn= connect

    def post(self, packetType, cmd, value=None, seq=None):
        '''按类型创建包对象，并按命令生成包体发送之'''
        packet=eval(packetType)(self.qc,value)
        self.conn.send(packet.newPacket(cmd,seq))

    def login(self):
        """登陆"""
        self.post('LoginPacket','0091')

    def chat(self):
        """与某人聊天"""
        num= '%08x'%input('请输入对方QQ号 >')
        print '--------------------'
        print '您正在和%s聊天'%int(num,16)
        print '按 回车 继续'
        print '输入 c 和其他好友聊'
        print '输入 x 返回命令菜单'
        print '--------------------'
        key=''
        while key!='x':
            if key=='c':
                num= '%08x'%input('请输入对方QQ号 >')
            self.post('MsgPacket','00cd',num)
            key=raw_input()

    def logout(self):
        for i in xrange(4):
            self.post('LogOutPacket','0062')

    def alive(self):
        """在线保持"""
        self.post('AlivePacket','0058')
