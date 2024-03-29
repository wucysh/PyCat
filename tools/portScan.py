#!/usr/bin/env python

import telnetlib
import threading
import queue


def get_ip_status(ip):
    server = telnetlib.Telnet()
    for port in range(80, 65535):
    # for port in [3306, 1521]:
        try:
            server.open(ip, port, 2)
            print('{0} port {1} is open'.format(ip, port))
        except Exception as err:
            print('{0} port {1} is not open'.format(ip, port))
            pass
        finally:
            server.close()


def check_open(q):
    try:
        while True:
            ip = q.get_nowait()
            get_ip_status(ip)
    except queue.Empty as e:
        pass


if __name__ == '__main__':
    host = ['40.73.64.124']  # 这里模拟多IP地址的情况，也可以从文件中读取IP——list
    q = queue.Queue()
    for ip in host:
        q.put(ip)
    threads = []
    for i in range(10):
        t = threading.Thread(target=check_open, args=(q,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()