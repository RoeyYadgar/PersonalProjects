# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 00:09:54 2021

@author: User
"""

import socket 
import struct
header = 4


def read(s):
    msg_length_bytes = s.recv(header)
    msg_length = struct.unpack('=I', msg_length_bytes)[0]
    msg = s.recv(msg_length).decode('utf-8')
    return msg


def send(s,msg):
    
    msg = msg.encode('utf-8')
    msg_length=  struct.pack('=I', len(msg))
    s.send(msg_length)
    s.send(msg)