#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       Hoho.py
#
# Copyright 2009 Seamile <lanhuermao@gmail.com>

import threading,sys
from binascii import b2a_hex
from time import sleep
from packet.inpacket import InPacket
import libqq,network,client

class RecvThread(threading.Thread):
    """消息接收线程"""
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock= sock
        self.recvData= []
        self.notify= threading.Event()

        self.name='Recver'
        self.setDaemon(1)
        self.start()

    def run(self):
        while 1:
            try:
                buf= b2a_hex( self.sock.recv(1024) )
                self.recvData.append(buf)
            except:
                print "接收时发生异常:",sys.exc_info()[0],sys.exc_info()[1]
            if self.recvData:
                self.notify.set()

class ParseThread(threading.Thread):
    """消息发送线程"""
    def __init__(self,client, connect, handle, recvThread):
        threading.Thread.__init__(self)
        self.qc=client
        self.conn=connect
        self.handle= handle
        self.recver= recvThread

        self.name='Parser'
        self.setDaemon(1)
        self.start()

    def run(self):
        while 1:
            self.recver.notify.wait()
            self.recver.notify.clear()

            packet= self.recver.recvData.pop(0)
            reply=InPacket(self.qc,self.conn).parse(packet)
            if reply:
                self.handle.post(reply[0],reply[1],reply[2],reply[3])
            if self.recver.recvData:
                self.recver.notify.set()

class inputThread(threading.Thread):
    """CMD处理器"""
    def __init__(self, handle):
        threading.Thread.__init__(self)
        self.handle= handle

        self.name='Inputer'
        self.setDaemon(1)
        self.start()

    def showCmdLst(self):
        print 'Hoho命令列表:'
        print 'chat：    聊天'
        print 'help：    查看命令列表'
        print 'exit：    退出QQ'
        print '************************'

    def run(self):
        InPacket.logged.wait()
        self.showCmdLst()
        cmdDict={
                'chat' :self.handle.chat,
                'c' :self.handle.chat,
                'help' :self.showCmdLst,
                'q' :self.handle.logout
                }
        cmd=''
        while cmd != 'q':
            cmd= raw_input('Hoho >>>').lower()
            try:
                cmdDict[cmd]()
            except:
                if cmd !='':print '没有该命令'

class AliveThread(threading.Thread):
    def __init__(self, handle):
        threading.Thread.__init__(self)
        self.handle= handle

        self.name='Aliver'
        self.setDaemon(1)
        self.start()
    def run(self):
        InPacket.logged.wait()
        while 1:
            self.handle.alive()
            sleep(20)

def main():
    """主函数"""
    # 对象初始化
    qc= client.Client()
    conn= network.Connect()
    handle= libqq.Protocol(qc, conn)
    # 启动接收和解析线程
    recver= RecvThread(conn.sock)
    parser= ParseThread(qc, conn, handle, recver,)
    # 登陆
    handle.login()
    #启动计时线程
    aliver= AliveThread(handle)
    #启动命令输入线程
    inputer=inputThread(handle)
    inputer.join()

if __name__ == '__main__':main()
