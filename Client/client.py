import socket
import sys
import time

from threading import Thread
from SocketServer import ThreadingMixIn

TCP_IP = '172.31.0.1'
TCP_PORT = 5222
BUFFER_SIZE = 1024

class ClientThread(Thread):
    
    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        
    def run(self): 
        data = self.sock.recv(BUFFER_SIZE)
        print 'Client connected to Server\r\n'
        cmd = data[0:3]
        if(cmd == '220'):
            print data[4:]
        while True:
            cmd = raw_input("cmd$ ")
            try:
                func = getattr(self, cmd[0:4].strip().upper())
                func(cmd)
            except Exception, e:
                print 'Error:', e


    def READ(self, cmd):
        self.sock.send(cmd)
        data = self.sock.recv(BUFFER_SIZE)
        print 'DATA READ IS:\r\n'
        print data

    def HELP(self, cmd):
        print 'cmd              : Action undertaken'
        print '------------------------------------'
        print 'list             : Lists all Bluetooth node devices in the Server\n'
        print 'scan             : Scans for the devices again and updates the table\n'
        print 'read(deviced_id) : reads the data from the bluetooth device with the specified ID\n'
   
    def SCAN(self, cmd):
        print 'Scanning for Bluetooth devices again ...'
        self.sock.send(cmd)
        data = self.sock.recv(BUFFER_SIZE)
        if(data[0:3] == '300'):
            print "Scanned for devices again, use 'list' command to list the devices"

    def LIST(self, cmd):
        self.sock.send(cmd)
        data = ''
        data = self.sock.recv(BUFFER_SIZE)
        #print data
        if(data[0:3] == '150'):
            recv_len = int(data[4:9])
        
        print "Length is :", recv_len
            
        while len(data) < recv_len:
            recv_data = self.sock.recv(BUFFER_SIZE)
            data = data + recv_data
            #print data
            
        print "============="
        print "Devices List:"
        print "============="
        
        data = data[10:]
        data_list = data.split("\n")
        for i in data_list:
            print i

if __name__ == '__main__':
    threads = []
    print 'Client booting ...'
    ipop_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipop_sock.connect((TCP_IP, TCP_PORT))
    print 'Client Trying Connection to :', TCP_IP
    client = ClientThread(TCP_IP, TCP_PORT, ipop_sock)
    client.daemon = True
    client.start()
    
    threads.append(client)

    while True:
            time.sleep(1)

    for t in threads:
        t.join()

