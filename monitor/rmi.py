import telnetlib

uri = "rmi://10.200.253.57:60016/dsmsService"
name = "dsmsService"

try:
    server = telnetlib.Telnet()
    # tn.read_until("login: ")
    # tn.write(user + "\n")
    # if password:
    #   tn.read_until("Password: ")
    #   tn.write(password + "\n")
    # tn.write("ls\n")
    # tn.write("exit\n")
    server.open("10.200.253.57", 60018)
    print(server)
except Exception as e:
    print(e)