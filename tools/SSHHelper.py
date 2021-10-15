# coding=utf-8
# !/usr/bin/python
import paramiko
import threading
"""
 ssh 到服务器并执行bash command 
"""


def ssh2(ip, username, passwd, cmd):
    """
    ssh 服务器并执行bash command
    :param ip:
    :param username:
    :param passwd:
    :param cmd:
    :return:
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd, timeout=5)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m + ' 2>&1', get_pty=True)
            #           stdin.write("Y")   #简单交互，输入 ‘Y’
            stdin.write("pwd\n")  # 简单交互，输入 ‘Y’

            # 实时输出
            while True:
                next_line = stdout.readline()
                if next_line == "":
                    break
                print(next_line, end='')
                # out = stdout.readlines()
                # # 屏幕输出
                # for o in out:
                #     print(o, end='')
                # 屏幕输出
                # for o in stderr.readlines():
                #     print(o, end='')
        print('%s\tOK\n' % (ip))
        ssh.close()
    except:
        print('%s\tError\n' % (ip))


def ssh2runbythread():
    """
    多线程 运行ssh2
    :return:
    """
    cmd = ['cal', 'echo hello!']  # 你要执行的命令列表
    username = ""  # 用户名
    passwd = ""  # 密码
    threads = []  # 多线程
    print("Begin......")
    for i in range(1, 254):
        ip = '192.168.1.' + str(i)
        a = threading.Thread(target=ssh2, args=(ip, username, passwd, cmd))
        a.start()


if __name__ == '__main__':
    ip = '0.0.0.0'
    username = 'user'
    passwd = 'pwd'

    cmd = [
        "cd /home/dm/azkaban && echo 'DDWUSER.T_DDW_DMN_CUST_INFO' > wucysh.txt",
        "cd /home/dm/azkaban && echo 'DDWUSER.T_DDW_F00_CUST_ASSET_TYPE_CURR' > wucysh.txt ",
    ]

    ssh2(ip, username, passwd, cmd)

