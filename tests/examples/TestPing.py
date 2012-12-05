# coding=utf-8

import socket
import struct
import argparse
from urllib.parse import urlparse

"""
Testing example implementing a ping tool for CoAP devices.
"""

def ping(url, maxNum=5, maxTime=5):
    def inms(t):
        return "%f ms" % t * 1000.0
    def ins(t):
        return "%f second" % t
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, timeout=maxTime)
    except Exception, e:
        print(type(e.reason))
    print("Trying #{maxnum} times with #{dest} at port #{port}, waiting #{ins(maxtime)} max:")
    for tentative in range(maxNum):
        sock.sendto([0b01000000, 0, tentative].pack("CCn"), 0)
        response, addr = socket.recvfrom(100)
        if len(response) != 4:
            print(response, addr)
        else:
            hd, code, seq = response.unpack("CCn")
            if hd != 0b01110000 or code != 0 or seq != n:
                print((inms(Time.now-t[seq]) ), [hd.to_s(2), code, seq], addr)
            else:
                print("#{%d % n} #{inms(Time.now - t[n])} #{addr[2]}")


ping("coap://coap.me:5683")
