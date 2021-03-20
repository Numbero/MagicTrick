from scp import SCPClient
import paramiko
import random
import os


TELE = 'XXX'
PASS = 'XXX'


def scp_upload(host, port, username, password, localpath, remotepath):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    scpclient = SCPClient(ssh.get_transport(), socket_timeout=15.0)
    scpclient.put(localpath, remotepath)    # 上传到服务器指定文件
    ssh.close()


if __name__ == '__main__':
    '''校园宽带自动连接脚本'''
    print()
    print('---------------------------------------')

    # 清理临时文件
    if os.path.isfile("network"):
        os.remove("network")
        print("| The 'network' has been deleted √    |")
    else:
        print("| Could not found the file 'network'! |")
    print('|                                     |')

    # 用户名和密码格式化
    username = "'tyxy#" + TELE + "'"
    netPassword = "'" + PASS + "'"

    # 生成MAC枚举数组
    eleLib = []
    for i in range(10):
        eleLib.append(str(i))
    for i in range(6):
        eleLib.append(chr(ord('a') + i))

    # 随机生成MAC地址
    mac = []
    mac.append("'")
    for i in range(6):
        for j in range(2):
            mac.append(eleLib[random.randint(0, 15)])
        if i != 5:
            mac.append(':')
    mac.append("'")
    mac = ''.join(mac)      # 将list转换为str
    print("| MAC address output:                 |")
    print('|     ' + mac + '             |')
    print('|                                     |')

    # 生成新的网络配置临时文件
    file = open("network", 'wb')
    text = """
config interface 'loopback'
    option ifname 'lo'
    option proto 'static'
    option ipaddr '127.0.0.1'
    option netmask '255.0.0.0'

config interface 'lan'
    option ifname 'eth2.2 eth2.3 eth2.4 eth2.5'
    option type 'bridge'
    option proto 'static'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    option macaddr 'cc:af:ee:b7:88:4a'

config interface 'wan'
    option ifname 'eth2.1'
    option _orig_ifname 'eth2.1'
    option _orig_bridge 'false'
    option proto 'pppoe'
"""
    text = text + "    option username " + username + '\n'
    text = text + "    option password " + netPassword + '\n'
    text = text + "    option macaddr " + mac + '\n' + '\n'
    file.write(bytes(text, encoding="utf8"))        # 将str转为byte
    file.close()

    # 路由器接口配置
    hostIp = "192.168.1.1"
    port = "22"
    username = "root"
    password = "XXX"

    # 上传配置文件
    local = "network"
    remote = "/etc/config/network"
    scp_upload(hostIp, port, username, password, local, remote)
    os.remove("network")
    print('| Upload configuration successfully √ |')

    # 发送SSH命令以刷新网络连接
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostIp, port, username, password)
    (stdin, stdout, stderr) = ssh.exec_command("ifup wan")
    ssh.close()
    print('| Send command successfully √         |')

    print('---------------------------------------')
    print()
