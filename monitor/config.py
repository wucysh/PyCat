#!/home/jack/miniconda2/envs/jack_conda/bin
# -*- coding: UTF-8 -*-

import utils

# staging
mysql_server="jdbc:mysql://127.0.0.1:60001/"
mysql_host = "127.0.0.1"
mysql_port = 60001
mysql_db = ""
mysql_user = ""
mysql_password = ""

#local_ip = utils.getIp()
local_ip = utils.get_host_ip()

default_sleep = 1200  # 如果系统没配置，默认睡眠20分钟
format_size = 1000000

print(local_ip)
