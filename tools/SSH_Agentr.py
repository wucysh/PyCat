import pexpect
"""
开启本机ssh 隧道

"""


def sudo(ssh_cmd, passwd):
    message = "error"
    ret = -1
    ssh = pexpect.spawn(ssh_cmd)
    try:
        i = ssh.expect(['continue connecting (yes/no)?', 'password:'], timeout=5)
        ssh.sendline('yes\n')
        i = ssh.expect(['password:'], timeout=5)
        ssh.sendline(passwd)
        # ssh.expect(pexpect.EOF)
        # print ssh.before
        # print ssh.after
        r = ssh.read()
        message = r
        ret = 0
    except pexpect.EOF:
        message = ""
        ret = 0
    except pexpect.TIMEOUT:
        message = "timeout"
        ret = -2
    finally:
        ssh.close()
    return ret, message

if __name__ == '__main__':

    ssh_cmd = "ssh -N -f -L 44040:0.0.0.0:4040 dm@0.0.0.0"
    passwd = "pwd"

    cmd_agent_str = """
    ps -ef |grep 43306 |grep -v grep |awk '{print $2}'|xargs kill -9
    ssh -N -f -L 44040:0.0.0.0:4040 dm@0.0.0.0
    """
    for cmd in cmd_agent_str.split('\n'):
        cmd = cmd.strip()
        if cmd == '':
            continue
        print(cmd)
        ret, message = sudo(cmd, passwd)
        print(ret, message)
