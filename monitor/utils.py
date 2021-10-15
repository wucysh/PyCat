#!/home/jack/miniconda2/envs/jack_conda/bin
# -*- coding: UTF-8 -*-
import socket


def getIp():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
