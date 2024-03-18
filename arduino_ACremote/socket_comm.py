# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 00:09:54 2021

@author: User
"""

import socket 
import math
header = 2


def read(s):
    msg_length_bytes = s.recv(header)
    msg_length = (msg_length_bytes[0] << 8) + msg_length_bytes[1]
    msg = s.recv(msg_length).decode('utf-8')
    return msg


def send(s,msg):
    
    msg_len = len(msg)
    s.send(bytes([math.floor(msg_len/256), msg_len%256]))
    s.send(msg.encode())