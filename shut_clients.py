#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from paramiko import SSHClient
import paramiko, time, getpass

def shut_clients(ips,senha):
	# senha = getpass.getpass()	
	ssh = SSHClient()

	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	k = paramiko.RSAKey.from_private_key_file("/home/servidor_lib/.ssh/id_rsa")
	for ip in ips:
		if ip != "não disponível":
			ssh.connect(ip, username="client_lib", pkey=k)

			ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo shutdown now", get_pty=True)
			ssh_stdin.write(senha + "\n")
			ssh_stdin.flush()
			
			print("fez",ssh_stdout.read())
			ssh.close()

