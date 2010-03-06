#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       inpacket.py
#
# Copyright (c) 2009-2015 Seamile <lanhuermao@gmail.com>

import struct, data, threading
from binascii import a2b_hex
from crypt import decrypt
from basicpacket import Packet

class InPacket(Packet):
    """解析接收包"""
    sequences=[]
    repackets=[]
    logged=threading.Event()
    def __init__(self,client,connect):
        Packet.__init__(self)
        self.qc= client
        self.conn= connect
        self.seq= ''

    def ip_h2d(self, newIP):
        """把十六进制的ip元组，转换成十进制数字形式的字符串"""
        lst=[]
        for s in newIP:
            lst+=[str(int(s,16))]
        return '.'.join(lst)

    def getCmd(self,packet):
        return packet[6:10]

    def getSeq(self,packet):
        return packet[10:14]

    def getBody(self,packet):
        return packet[14:-2]

    def parse(self, packet):
        '''解析接收包'''
        self.seq= self.getSeq(packet)
        if self.seq not in InPacket.sequences:
            InPacket.sequences.append(self.seq)
            if self.seq not in Packet.sequences:
                Packet.sequences.append(self.seq)
            cmd= self.getCmd(packet)
            body= self.getBody(packet)
            try:
                return getattr(self,'unpack_%s'%cmd)(body)
            except:
                pass
        else:
            if self.seq not in InPacket.repackets:
                InPacket.repackets.append(self.seq)

    def unpack_0091(self, body):
        decrypted= decrypt(body, data.loginData['krand'])
        ok= decrypted[-2:]
        if ok=='00':
            fmt= '2s 8s 8s 16s 116s 2s'
            decrypted= struct.unpack(fmt, decrypted)
            self.qc.time= decrypted[1]
            self.qc.myip= decrypted[2]
            data.loginData['tk91']= decrypted[4]
            return 'LoginPacket','00ba',None,None
        else:
            new_ip= struct.unpack('2s 2s 2s 2s',decrypted[len(decrypted)-8:])
            self.conn.host=self.ip_h2d(new_ip)
            return 'LoginPacket','0091',None,None

    def unpack_00ba(self, body):
        decrypted= decrypt(body, data.loginData['krand'])
        verify= decrypted[8:16]
        if verify=='00000000':
            data.loginData['tkba']= decrypted[16:]
            return 'LoginPacket','00dd',None,None
        else:
            pp= a2b_hex(decrypted[52:700])
            fd = file('../pp.png', 'wb')
            fd.write(pp)
            fd.close()
            return 'LoginPacket','00ba','verify',None

    def unpack_00dd(self, body):
        decrypted= decrypt(body, self.qc.md5ps1)

        fmt='10s 372s 116s 32s 4s 32s 4s'
        decrypted= struct.unpack(fmt, decrypted)
        data.loginData['tkdd']= decrypted[1],decrypted[2]
        data.loginData['kdd']= decrypted[3],decrypted[5]
        return 'LoginPacket','00e5',None,None

    def unpack_00e5(self, body):
        decrypted= decrypt(body, data.loginData['kdd'][1])

        fmt='8s 32s 24s 8s 16s 372s'
        decrypted= struct.unpack(fmt, decrypted[:460])
        data.loginData['ke5']= decrypted[1]
        self.qc.time= decrypted[3]
        data.loginData['tke5']= decrypted[5]
        return 'LoginPacket','0030',None,None

    def unpack_0030(self, body):
        decrypted= decrypt(body, data.loginData['ke5'])
        self.qc.sessionkey= struct.unpack('32s', decrypted[2:34])[0]
        InPacket.logged.set()
        print '登陆成功！\n'

    def unpack_00ce(self, body):
        decoded= decrypt(body, self.qc.sessionkey)
        if len(decoded) > 138:
            buddyID= int(decoded[0:8],16)
            for i in xrange(len(decoded)):
                if decoded[i:i+6]=='4d5347':
                    msg=decoded[i+80:]
            try:
                msg= a2b_hex(msg).decode('utf8')
                print '好友',buddyID,'对你说:',msg
            except:
                pass
        return 'MsgPacket','0017',decoded[:32],self.seq

    def unpack_00cd(self, body):
        '''好友收到消息的应答
        有待改进，发送端如果长时间未收到对应seq的这个应答包，要提示消息未收到'''
        decoded= decrypt(body, self.qc.sessionkey)

    def unpack_0017(self, body):
        '''功能似乎和收到的CD包一样'''
        decoded= decrypt(body, self.qc.sessionkey)

    def unpack_0058(self,body):
        decoded= decrypt(body, self.qc.sessionkey)
        if decoded[:2] != '00':
            return 'AlivePacket','0058',None,None
