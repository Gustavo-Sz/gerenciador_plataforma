import os

def get_macs():
    curdir = os.getcwdb().decode('utf-8')
    file = open(curdir + "//mac_addresses",'r')
    mac_addresses = file.readlines()
    mac_addresses = [mac.strip() for mac in mac_addresses]
    file.close()
    return mac_addresses