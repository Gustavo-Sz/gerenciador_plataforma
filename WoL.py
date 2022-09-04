#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import struct

'''
local_ip = socket.gethostbyname(socket.gethostname())

local_ip = local_ip.rsplit('.', 1)
local_ip[1] = '255'
broadcast_ip = '.'.join(local_ip)
print(broadcast_ip)
'''
#("FC:34:97:7A:DD:9C","FC:34:97:7A:DB:4E")
def wol(macs):
	# print(macs)
	for mac_address in macs: 
		# print(f"Iniciando máquina com MAC: {mac_address}\n")

		mac_address = mac_address.replace(mac_address[2], '')

		# Pad the synchronization stream.
		data = ''.join(['FFFFFFFFFFFF', mac_address * 20])
		send_data = b''

		# Split up the hex values and pack.
		for j in range(0, len(data), 2):
		    send_data = b''.join([
			send_data,
			struct.pack('B', int(data[j: j + 2], 16))
		    ])

		# Broadcast it to the LAN.
		
		sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		sock.sendto(send_data, ("192.168.88.255", 7))
		
