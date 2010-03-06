#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       network.py
#
# Copyright (c) 2009-2015 Seamile <lanhuermao@gmail.com>

import socket

class Connect:
    def __init__(self):
        self.sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(180)
        self.host= 'sz.tencent.com'
        self.port= 8000
        self.myip= ''
        self.myport= ''

    def send(self, data):
        self.sock.sendto(data,(self.host,self.port))
